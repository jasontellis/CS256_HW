Please run jason_tellis_job_environment.py without any arguments

Help file has been implemented and can be accessed by specifying python jason_tellis_job_environment.py -h
Intelligently re-generates lookup file table on disk on a daily basis
Stores lookup table as list of jobs hashed by search string and sorted on Jaccard distances of vector containing job title, description and location from search string
Removes stopwords and special characters from retrieved documents and stores vector as frequency count of words in job title, description and location
Displays results both on command line as well as a formatted HTML table

Uses modularized logic to fetch jobs from all 3 websites without writing duplicate code
builds Lookup table only if no jobs found for search string in lookuptable on disk
Unfortunately, could not implement k-means clustering