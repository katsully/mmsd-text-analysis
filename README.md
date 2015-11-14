# mmsd-text-analysis
This is a twitter bot that responds to #firstworldproblems tweets with news stories from developing world countries. 

To automate the script we are using crontab.

To create a crontab script, opened terminal and type

	crontab -e
	
This will open up vim. In vim, type

    */10 * * * * cd Path/to/this/directory && python text_analysis.py
    
This will run the python script every ten minutes.

### API Keys

You will need two sets of API keys, one for the New York Times and one for Twitter. Store the Twitter keys in a text file named twitter\_keys.txt and store the New York Times API key in a text file named ny\_times\_key.txt