# NV_batch
Batch file to generate WSOR figures for NV. This is reproducible, allowing anyone with Python installed on their local machine to generate these figures.

Before running it, there are some setup steps that must be taken. Please read through all steps before doing anything.

## Setup Instructions (first time only)

1. Make sure you have Python downloaded. You can download it from the Software Center. The newest version will be fine (3.12 at this time).
2. If using GitHub, clone the NV_batch repository to your local machine. If you received NV_batch as a zip file, unzip this folder wherever you want it to live.
3. In File Explorer, right click the path for the NV_batch folder and copy it as text.
4. Open Command Prompt and change directory to your copied file path by typing cd followed by a space and then pasting your file path

cd paste_file_path

6. Hit enter. Command Prompt should now show the full path of the NV_batch folder.
7. Copy and paste the following three lines, hitting enter after each one:

python -m venv WSOR_NV_env

WSOR_NV_env\Scripts\activate

pip install -r requirements.txt

6. When the code runs, it will save the generated figures into a few locations. You need to make sure these folders exist beforehand. <br>
Create the following folders (exact wording) at the specified path if they don't already exist:

C:\USDA\Work\ReportDocs\Jeff_WSOR_Docs\Figs

C:\USDA\Work\ReportDocs\Jeff_WSOR_Docs\PDFs

C:\USDA\Work\ReportDocs\Jeff_WSOR_Docs\WordDocs

## Configuration (every time you generate the report for a new month/year)
1. Open config.txt in notepad or whatever text editor you prefer and set the ReportYear and ReportMonth appropriately
2. Save and close the config file.

## Running the Pipeline
Simply double-click **GenerateReport.bat** 

A Command Prompt window will open, keeping you updated on progress and alerting you of any errors.

## Troubleshooting
The most likely issue you will run into is if you try to run the .bat file (which generates word docs, figures, and pdfs) if you have MS Word or one of the files you are trying to write open. <br>
Make sure to close down Word, Adobe, and any figure files before running.


