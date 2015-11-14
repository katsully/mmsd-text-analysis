# mmsd-text-analysis
This is a twitter bot that responds to #firstworldproblems tweets with news stories from developing world countries. 

To automate the script we are using crontab.

To create a crontab script, opened terminal and type

	crontab -e
	
This will open up vim. In vim, type

    */10 * * * * cd Path/to/this/directory && python text_analysis.py
    
This will run the python script every ten minutes.