from playwright.sync_api import Playwright, sync_playwright, expect
import time
from dateutil import parser
import datetime
import signal



reminders_for_work = [{'method': 'popup', 'minutes': 90}, {'method': 'popup', 'minutes': 150}, {'method': 'popup', 'minutes': 60}]


def parse_schedule(schedule):
    # takes output from run_mytime and parses it into a
    events = []
    for day in schedule:
        lines = day.split('\n\n')
        if len(lines) == 1:
            pass
        elif len(lines) >= 5:
            date = lines[0].split(',')[1][1:]
            start = lines[1]
            end = lines[3]
            Title = "Work at Target - " + lines[4]
            Description = lines[4]
            Location = "4616 US-280, Birmingham, AL, 35242"
            dt_start = parser.parse(date+' ' + start).isoformat()
            dt_end = parser.parse(date+' ' + end).isoformat()
            timezone = "US/Central"
            events.append({'summary':Title, 'start':{'dateTime':dt_start,'timeZone':timezone},
                           'end':{'dateTime':dt_end, 'timeZone':timezone},
                           'id':'vorkattarget'+date.lower().replace(' ', ''),
                           'description':Description, 'location':Location, 'reminders':{'useDefault':False, 'overrides': reminders_for_work}})
        else:
            pass
    return events


def run(playwright: Playwright, id, pw, headless=False) -> None:
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context(storage_state='auth.json')

    # Open new page
    page = context.new_page()

    # Go to https://mytime.target.com/
    page.goto("https://mytime.target.com/")

    # Go to https://logonservices.iam.target.com/v1/login/?application=wfm_tm_enablement_ui_prod_im&assurance=2&form=password&referrer=https%3A%2F%2Foauth.iam.target.com%2Fauth%2Foauth%2Fv2%2Fauthorize%3Fclient_id%3Dwfm_tm_enablement_ui_prod_im%26nonce%3Dbj1-NNwzNiEAhxaUBF7FP%26redirect_uri%3Dhttps%3A%2F%2Fmytime.target.com%26response_type%3Dtoken+id_token%26scope%3Dopenid+profile%26state%3D&tid=43be7f22-eec3-4729-80bf-8751c7d6dd66&type=teammember+partner
    # Not necesary, we get redirected here
    #page.goto("https://logonservices.iam.target.com/v1/login/?application=wfm_tm_enablement_ui_prod_im&assurance=2&form=password&referrer=https%3A%2F%2Foauth.iam.target.com%2Fauth%2Foauth%2Fv2%2Fauthorize%3Fclient_id%3Dwfm_tm_enablement_ui_prod_im%26nonce%3Dbj1-NNwzNiEAhxaUBF7FP%26redirect_uri%3Dhttps%3A%2F%2Fmytime.target.com%26response_type%3Dtoken+id_token%26scope%3Dopenid+profile%26state%3D&tid=43be7f22-eec3-4729-80bf-8751c7d6dd66&type=teammember+partner")

    # Click input[type="text"]
    page.locator("input[type=\"text\"]").click()

    # Fill input[type="text"]
    page.locator("input[type=\"text\"]").fill(id)

    # Press Tab
    page.locator("input[type=\"text\"]").press("Tab")

    # Fill input[type="password"]
    page.locator("input[type=\"password\"]").fill(pw)

    # Click button:has-text("Login")
    page.locator("button:has-text(\"Login\")").click()

    time.sleep(9)

    #print(page.locator("button:has-text(\"SMS\")").all_inner_texts())

    try:
        smsbuttoncount = page.locator('button:has(:text-is("SMS")').count()
        # handle occasionally getting the sms otp codes
    except Exception:
        print(Exception)
        smsbuttoncount = 0

    if smsbuttoncount > 0:

        # Click button:has-text("SMS******9026")
        page.locator("button:has-text(\"SMS\")").click()

        # Click input[type="password"]
        page.locator("input[type=\"password\"]").click()

        # Fill input[type="password"]
        otp = input("What is the OTP?")

        page.locator("input[type=\"password\"]").fill(otp)

        # Check input[type="checkbox"]
        page.locator("input[type=\"checkbox\"]").check()

        # Click button:has-text("Submit")
        # with page.expect_navigation(url="https://mytime.target.com/"):
        with page.expect_navigation():
            page.locator("button:has-text(\"Submit\")").click()

    # Click a[role="button"] >> nth=1

    time.sleep(.5)

    page.locator("a[role=\"button\"]").nth(1).click()
    # expect(page).to_have_url("https://mytime.target.com/schedule")

    schedule = page.locator("li").all_inner_texts()

    time.sleep(.5)

    # Click button >> nth=2
    page.locator("button").nth(2).click()

    schedule += page.locator("li").all_inner_texts()

    time.sleep(.5)

    # Click text=June 2022S12M13T14W15T16F17S18 >> button >> nth=1
    page.locator("button").nth(2).click()

    schedule += page.locator("li").all_inner_texts()

    time.sleep(.5)

    # Click text=June 2022S19M20T21W22T23F24S25 >> button >> nth=1
    page.locator("button").nth(2).click()

    schedule += page.locator("li").all_inner_texts()

    raunch = input("Enter a thing, I am blocking")

    # Click [aria-label="Menu"]
    page.locator("[aria-label=\"Menu\"]").click()

    # Click button:has-text("Logout")
    # with page.expect_navigation(url="https://logonservices.iam.target.com/v1/login/?application=wfm_tm_enablement_ui_prod_im&assurance=2&form=password&referrer=https%3A%2F%2Foauth.iam.target.com%2Fauth%2Foauth%2Fv2%2Fauthorize%3Fclient_id%3Dwfm_tm_enablement_ui_prod_im%26nonce%3D8I4cZeX0Y8Qh9EvJ4WaRM%26redirect_uri%3Dhttps%3A%2F%2Fmytime.target.com%26response_type%3Dtoken+id_token%26scope%3Dopenid+profile%26state%3D&tid=ff016eed-6113-4f90-a2eb-f5a63291f8c5&type=teammember+partner"):
    with page.expect_navigation():
        page.locator("button:has-text(\"Logout\")").click()
    # expect(page).to_have_url("https://logonservices.iam.target.com/login/responses/logoff.html?target=https%3A%2F%2Fmytime.target.com")

    # ---------------------
    context.storage_state(path="auth.json")
    context.close()
    browser.close()
    return schedule


def run_mytime(id, pw, headless=False):
    with sync_playwright() as playwright:
        return parse_schedule(run(playwright, id, pw, headless=headless))
