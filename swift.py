import re
import os
import argparse
import asyncio
from urllib.parse import urlparse
from collections import defaultdict
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from colorama import Fore, Style
from datetime import datetime
from report_generator import generate_html_report  # Import the function

async def fly_over(browser, url: str, project_folder: str, data: list, timeout: int):
    try:
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 1024}  # Set viewport size for desktop
        )
        page = await context.new_page()
        response = await page.goto(url, timeout=timeout)  # Set a timeout for navigation

        # Retrieve server header
        server_header = response.headers.get('server')

        # Create folder if it doesn't exist
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)

        # Generate a filename with appended number if it already exists
        safe_url = re.sub(r'[^a-zA-Z0-9]', '_', url)
        screenshot_name = os.path.join(project_folder, f"screenshot_{safe_url}.png")
        counter = 1
        while os.path.exists(screenshot_name):
            screenshot_name = os.path.join(project_folder, f"screenshot_{safe_url}_{counter}.png")
            counter += 1

        await page.screenshot(path=screenshot_name, full_page=True)
        await context.close()
        print(f"{Fore.GREEN}Screenshot saved for {url} as {screenshot_name}{Style.RESET_ALL}")

        data.append({'url': url, 'filename': screenshot_name, 'server_header': server_header})
    except PlaywrightTimeoutError:
        print(f"{Fore.RED}URL not reachable: {url}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred with URL {url}: {e}{Style.RESET_ALL}")

async def main(urls_file, num_contexts, project_folder, project_name, timeout):
    data = []
    removed_duplicates = set()  # To store removed duplicate URLs
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Dictionary to store URLs by domain
        domain_urls = defaultdict(list)

        with open(urls_file, "r") as file:
            urls = [url.strip() for url in file.readlines() if url.strip()]

        # Group URLs by domain
        for url in urls:
            domain = urlparse(url).netloc
            domain_urls[domain].append(url)

        # Flatten the dictionary values
        urls = [url for domain in domain_urls.values() for url in domain]

        # Create tasks for each URL
        tasks = []
        for url in urls:
            if url in removed_duplicates:
                print(f"{Fore.YELLOW}Duplicate URL removed: {url}{Style.RESET_ALL}")
                continue
            tasks.append(fly_over(browser, url, project_folder, data, timeout))
            removed_duplicates.add(url)
        
        # Run tasks concurrently with a limit on the number of concurrent contexts
        semaphore = asyncio.Semaphore(num_contexts)

        async def limited_task(task):
            async with semaphore:
                await task

        await asyncio.gather(*[limited_task(task) for task in tasks])

        await browser.close()

    generate_html_report(project_folder, project_name, data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process URLs and take screenshots.')
    parser.add_argument('-u', '--urls', type=str, required=True, help='Path to the URLs file')
    parser.add_argument('-c', '--contexts', type=int, default=4, help='Number of Playwright contexts to use (default: 4)')
    parser.add_argument('-p', '--project', type=str, default=None, help='Name of the project folder (default: timestamp)')
    parser.add_argument('-t', '--timeout', type=int, default=10000, help='Timeout for navigation in milliseconds (default: 10000)')
    args = parser.parse_args()

    if args.project is None:
        # Use timestamp as default project folder name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        project_folder = f"screenshots_{timestamp}"
        project_name = "Report"
    else:
        project_folder = args.project
        project_name = args.project

    asyncio.run(main(args.urls, args.contexts, project_folder, project_name, args.timeout))
