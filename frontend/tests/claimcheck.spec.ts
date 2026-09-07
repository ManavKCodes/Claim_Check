import { expect, test } from "@playwright/test";

test("reviewer can correct evidence and inspect an abstention result", async ({ page }) => {
  await page.route("http://localhost:8000/api/claim/extract", async (route) => {
    await route.fulfill({ json: { claim_type: "COMPARATIVE_PROTEIN" } });
  });
  await page.route("http://localhost:8000/api/verify", async (route) => {
    await route.fulfill({ json: {
      verification_id: "e2e-verification", claim_type: "COMPARATIVE_PROTEIN", verdict: "INSUFFICIENT_EVIDENCE",
      rule_id: "FSSAI-COMPARATIVE-PROTEIN-PENDING-001", rule_version: "PENDING_SOURCE_VERIFICATION",
      calculation: null, evidence_completeness: 0.25, missing_evidence: ["valid_comparator"], evidence: [],
    } });
  });
  await page.goto("/");
  await page.getByLabel("Raw claim text").fill("30% More Protein");
  await page.getByRole("button", { name: "Normalize" }).click();
  await expect(page.getByText("COMPARATIVE_PROTEIN")).toBeVisible();
  await page.getByLabel("Protein (g)").fill("26");
  await page.getByRole("button", { name: "Verify claim" }).click();
  await expect(page.getByRole("heading", { name: "INSUFFICIENT EVIDENCE" })).toBeVisible();
  await expect(page.getByText("valid_comparator")).toBeVisible();
});

test("connection errors are shown instead of becoming a verdict", async ({ page }) => {
  await page.route("http://localhost:8000/api/claim/extract", async (route) => {
    await route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ detail: "Backend unavailable" }) });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Normalize" }).click();
  await expect(page.getByText("Backend unavailable")).toBeVisible();
  await expect(page.locator(".result-panel")).toHaveCount(0);
});
