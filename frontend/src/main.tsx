import { FormEvent, StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type ClaimType = "HIGH_PROTEIN" | "LOW_FAT" | "NO_ADDED_SUGAR" | "COMPARATIVE_PROTEIN" | "REDUCED_SODIUM";
type Verdict = "SUPPORTED" | "CONTRADICTED" | "INSUFFICIENT_EVIDENCE";
type EvidenceField = { field_name: string; raw_value: string; normalized_value: string; unit?: string; source_type: string };
type VerificationResult = { verification_id: string; claim_type: string; verdict: Verdict; rule_id: string; rule_version: string | null; calculation: Record<string, unknown> | null; evidence_completeness: number; missing_evidence: string[]; evidence: EvidenceField[] };
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail ?? `Request failed (${response.status})`);
  return payload as T;
}

function App() {
  const [productName, setProductName] = useState("");
  const [barcode, setBarcode] = useState("");
  const [claimText, setClaimText] = useState("High Protein");
  const [claimType, setClaimType] = useState<ClaimType | "">("HIGH_PROTEIN");
  const [protein, setProtein] = useState("");
  const [fat, setFat] = useState("");
  const [sodium, setSodium] = useState("");
  const [ingredients, setIngredients] = useState("");
  const [comparatorStatus, setComparatorStatus] = useState("NO_VALID_COMPARATOR");
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [message, setMessage] = useState("Review the extracted fields, correct them, then verify.");
  const [busy, setBusy] = useState(false);

  async function extractClaim() {
    setMessage("Reading claim text...");
    try {
      const response = await request<{ claim_type: ClaimType | null }>("/api/claim/extract", { raw_text: claimText, source: "user_review" });
      setClaimType(response.claim_type ?? "");
      setMessage(response.claim_type ? "Claim normalized. Check the evidence fields before verifying." : "Claim is ambiguous. Correct the claim text before verifying.");
    } catch (error) { setMessage(error instanceof Error ? error.message : "Claim extraction failed."); }
  }

  async function lookupProduct(event: FormEvent) {
    event.preventDefault();
    if (!barcode.trim()) return setMessage("Enter a barcode to look up product data.");
    setBusy(true);
    try {
      const response = await request<{ name?: string; ingredients_text?: string; nutriments?: Record<string, number> }>("/api/product/lookup", { barcode });
      const nutrition = response.nutriments ?? {};
      setProductName(response.name ?? ""); setIngredients(response.ingredients_text ?? ""); setProtein(nutrition.proteins_100g?.toString() ?? ""); setFat(nutrition.fat_100g?.toString() ?? ""); setSodium(nutrition.sodium_100g?.toString() ?? "");
      setMessage("Product data loaded. Review every value before verification.");
    } catch (error) { setMessage(error instanceof Error ? error.message : "Product lookup failed."); }
    finally { setBusy(false); }
  }

  async function verify(event: FormEvent) {
    event.preventDefault();
    if (!claimType) return setMessage("Normalize a supported claim before verifying.");
    setBusy(true);
    const evidence: EvidenceField[] = [{ field_name: "claim", raw_value: claimText, normalized_value: claimText, source_type: "user_review" }];
    const addNumeric = (field_name: string, value: string) => { if (value.trim()) evidence.push({ field_name, raw_value: value, normalized_value: value, unit: "g", source_type: "user_review" }); };
    addNumeric("subject_protein", protein); addNumeric("subject_fat", fat); addNumeric("subject_sodium", sodium);
    if (ingredients.trim()) evidence.push({ field_name: "ingredient_list", raw_value: ingredients, normalized_value: ingredients, source_type: "user_review" });
    try {
      const response = await request<VerificationResult>("/api/verify", { claim_type: claimType, raw_claim: claimText, evidence, comparator_status: comparatorStatus, comparator_details: { basis: "per_100g", product_name: productName } });
      setResult(response); setMessage("Verification complete. Inspect the rule, calculation, and missing evidence below.");
    } catch (error) { setMessage(error instanceof Error ? error.message : "Verification failed."); }
    finally { setBusy(false); }
  }

  return (
    <main className="app-shell">
      <header className="topbar"><div><p className="eyebrow">Evidence screening / India</p><h1>ClaimCheck</h1></div><span className="phase-pill">Review workspace</span></header>
      <div className="workspace">
        <section className="panel"><div className="section-heading"><span className="step">01</span><div><h2>Identify the product</h2><p>Start with a barcode, then inspect the retrieved fields.</p></div></div><form className="lookup" onSubmit={lookupProduct}><label>Barcode<input value={barcode} onChange={(event) => setBarcode(event.target.value)} placeholder="e.g. 8901234567890" inputMode="numeric" /></label><button className="button secondary" disabled={busy} type="submit">{busy ? "Loading..." : "Look up product"}</button></form><label>Product name<input value={productName} onChange={(event) => setProductName(event.target.value)} placeholder="Editable product name" /></label></section>
        <section className="panel"><div className="section-heading"><span className="step">02</span><div><h2>Review the claim</h2><p>Extraction is a candidate. You remain in control of the correction.</p></div></div><div className="claim-row"><label>Raw claim text<input value={claimText} onChange={(event) => setClaimText(event.target.value)} /></label><button className="button secondary compact" onClick={extractClaim} type="button">Normalize</button></div><div className="classification"><span className="label">Normalized type</span><strong>{claimType || "Unclassified"}</strong></div></section>
        <section className="panel"><div className="section-heading"><span className="step">03</span><div><h2>Inspect evidence</h2><p>Correct values before they enter the deterministic engine. Basis: per 100 g.</p></div></div><div className="field-grid"><label>Protein (g)<input value={protein} onChange={(event) => setProtein(event.target.value)} placeholder="Missing stays missing" inputMode="decimal" /></label><label>Fat (g)<input value={fat} onChange={(event) => setFat(event.target.value)} placeholder="Missing stays missing" inputMode="decimal" /></label><label>Sodium (g)<input value={sodium} onChange={(event) => setSodium(event.target.value)} placeholder="Missing stays missing" inputMode="decimal" /></label></div><label>Ingredients<input value={ingredients} onChange={(event) => setIngredients(event.target.value)} placeholder="Paste or correct the ingredient list" /></label><label>Comparator status<select value={comparatorStatus} onChange={(event) => setComparatorStatus(event.target.value)}><option value="NO_VALID_COMPARATOR">No valid comparator</option><option value="AMBIGUOUS_COMPARATOR">Ambiguous comparator</option><option value="MATCHED">Matched comparator</option></select></label></section>
        <section className="action-bar"><p role="status">{message}</p><button className="button primary" disabled={busy} onClick={verify} type="button">{busy ? "Verifying..." : "Verify claim"}</button></section>
        {result && <section className={`result-panel verdict-${result.verdict.toLowerCase()}`} aria-live="polite"><div className="result-head"><div><p className="eyebrow">Verification result</p><h2>{result.verdict.replace(/_/g, " ")}</h2></div><div className="score"><strong>{Math.round(result.evidence_completeness * 100)}%</strong><span>evidence complete</span></div></div><div className="result-grid"><div><span className="label">Claim type</span><strong>{result.claim_type}</strong></div><div><span className="label">Rule</span><strong>{result.rule_id}</strong><small>{result.rule_version ?? "Version unavailable"}</small></div><div><span className="label">Calculation</span><strong>{result.calculation ? JSON.stringify(result.calculation) : "Not calculated"}</strong></div><div><span className="label">Missing evidence</span><strong>{result.missing_evidence.length ? result.missing_evidence.join(", ") : "None recorded"}</strong></div></div><p className="legal">ClaimCheck is an evidence-screening tool and not a legal certification.</p></section>}
      </div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

if ("serviceWorker" in navigator && import.meta.env.PROD) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/service-worker.js").catch(() => {
      // The app remains usable when service-worker registration is unavailable.
    });
  });
}
