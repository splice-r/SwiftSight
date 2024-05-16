# SwiftSight
AI developed tool used to perform domain flyovers.
Code was written mainly through ChatGPT. It leverages Playwright in order to automate the process of opening a list of URLs and taking a screenshot of the page.
Additionally, it creates a HTML report file with the screenshot that was taken and the "Server" response header.

## Installation
- clone repository (`git clone https://github.com/splice-r/SwiftSight.git`)
- cd SwiftSight
- install requirements (`pip install -r requirements.txt`)

## Usage
Example: `python swift.py -u urls.txt -p TestProject`
Help: `python swift.py -h`

## Features
- Eliminates URL duplicates from input list
- Generates report with taken screenshots and highlights Server header

## Credits and inspiration
- [Aquatone](https://github.com/michenriksen/aquatone)
- [gowitness](https://github.com/sensepost/gowitness)
