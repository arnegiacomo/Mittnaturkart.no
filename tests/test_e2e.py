#!/usr/bin/env python3
import time
import sys
from playwright.sync_api import sync_playwright, expect

BASE_URL = "http://nginx"

def wait_for_app(page, max_retries=30):
    print("Waiting for application to be ready...")
    for i in range(max_retries):
        try:
            page.goto(BASE_URL, timeout=5000)
            page.wait_for_selector("h1", timeout=3000)
            print(f"✓ Application is ready after {i+1} attempts")
            return True
        except Exception:
            time.sleep(1)
    print("✗ Application failed to start")
    return False

def test_page_loads(page):
    print("\n--- Testing Page Load ---")
    page.goto(BASE_URL)

    # Check header exists
    expect(page.locator("h1")).to_contain_text("Mitt Naturkart")
    print("✓ Page header found")

    # Check button exists
    expect(page.get_by_role("button", name="Ny observasjon")).to_be_visible()
    print("✓ 'Ny observasjon' button visible")

def test_create_observation(page):
    print("\n--- Testing Create Observation ---")
    page.goto(BASE_URL)

    # Click "Ny observasjon" button
    page.get_by_role("button", name="Ny observasjon").click()

    # Wait for dialog to appear
    page.wait_for_selector('[role="dialog"]', timeout=5000)
    print("✓ Dialog opened")

    # Fill in the form
    page.locator('input[id="species"]').fill("Granskog fugl")

    # Click the Select dropdown for category (PrimeVue Select has a complex structure)
    page.locator('#category').click()
    page.wait_for_timeout(500)  # Wait for dropdown to open
    page.locator('[role="option"]').first.click()  # Select first option (Fugl)

    # No location fields - observations can be created without a location

    # Fill notes
    page.locator('textarea[id="notes"]').fill("E2E test observation")
    print("✓ Form filled")

    # Submit the form
    page.get_by_role("button", name="Lagre").click()

    # Wait for success toast
    page.wait_for_selector(".p-toast", timeout=5000)
    expect(page.locator(".p-toast")).to_contain_text("Opprettet")
    print("✓ Observation created successfully")

    # Verify observation appears in table
    expect(page.get_by_text("Granskog fugl")).to_be_visible()
    print("✓ Observation visible in table")

def test_edit_observation(page):
    print("\n--- Testing Edit Observation ---")
    page.goto(BASE_URL)

    # Wait for table to load
    page.wait_for_selector("table", timeout=5000)

    # Click edit button (pencil icon) - PrimeVue buttons have the icon as child
    page.locator('button:has(.pi-pencil)').first.click()

    # Wait for dialog
    page.wait_for_selector('[role="dialog"]', timeout=5000)
    print("✓ Edit dialog opened")

    # Update notes field
    page.locator('textarea[id="notes"]').fill("Updated E2E test observation")

    # Save
    page.get_by_role("button", name="Lagre").click()

    # Wait for success toast
    page.wait_for_selector(".p-toast", timeout=5000)
    expect(page.locator(".p-toast")).to_contain_text("Oppdatert")
    print("✓ Observation updated successfully")

def test_delete_observation(page):
    print("\n--- Testing Delete Observation ---")
    page.goto(BASE_URL)

    # Wait for table to load
    page.wait_for_selector("table", timeout=5000)

    # Click delete button (trash icon)
    page.locator('button:has(.pi-trash)').first.click()

    # Wait for PrimeVue confirmation dialog (uses .p-confirmdialog class)
    page.wait_for_selector(".p-confirmdialog", timeout=5000)
    print("✓ Confirmation dialog opened")

    # Confirm deletion by clicking "Ja" button
    page.locator('.p-confirmdialog').get_by_role("button", name="Ja").click()

    # Wait for success toast
    page.wait_for_selector(".p-toast", timeout=5000)
    expect(page.locator(".p-toast")).to_contain_text("Slettet")
    print("✓ Observation deleted successfully")

def run_tests():
    print("=" * 50)
    print("Starting Frontend E2E Tests")
    print("=" * 50)

    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            if not wait_for_app(page):
                return 1

            test_page_loads(page)
            test_create_observation(page)
            test_edit_observation(page)
            test_delete_observation(page)

            print("\n" + "=" * 50)
            print("✓ All E2E tests passed!")
            print("=" * 50)

            browser.close()
            return 0

        except Exception as e:
            print(f"\n✗ Test failed: {e}")
            browser.close()
            return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
