# NV_batch
Batch file to generate WSOR figures for NV. This is reproducible, allowing anyone with Python installed on their local machine to generate these figures.

Before running it, there are some setup steps that must be taken.

## Setup Instructions (first time only)

1. Create a new folder called NV_batch wherever you want this script to live.<br>
Wherever you unzipped this zip file will work. If you created a GitHub repository for this, use that location.
2. In File Explorer, right click the path for this folder and copy it.
3. Open Command Prompt and type: cd
4. Paste file path (with a space after cd) and hit enter. Command Prompt should now show the full path of the NV_batch folder
5. Copy and paste the following three lines, hitting enter after each one:

python -m venv WSOR_NV_env

WSOR_NV_env\Scripts\activate

pip install -r requirements.txt

6. When the code runs, it will save the generated figures into a few locations. You need to make sure these folders exist beforehand. <br>
Create the following folders at the specified path if they don't already exist:

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


