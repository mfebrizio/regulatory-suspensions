# regulatory-suspensions

*Overview:*

[Regulatory suspensions](https://www.theregreview.org/2020/03/16/davis-noll-revesz-regulatory-rollbacks-changed-nature-presidential-power/) "defer compliance by either postponing the compliance dates or putting off a regulation’s effective date, prior to working to change or repeal the regulation’s substantive requirements." Suspensions are one of [several mechanisms](https://regulatorystudies.columbian.gwu.edu/biden-using-multiple-mechanisms-reverse-trumps-regulatory-agenda) that incoming presidents use to reverse the regulatory agenda of the prior administration. Federal agencies publish these postponements in the [Federal Register](https://www.federalregister.gov/), the daily journal of the US government. Understanding the frequency of regulatory suspensions across presidential administrations may help contextualize the usage of this tool of regulatory oversight. Our objective is to identify regulatory suspensions and analyze how presidential administrations use them differently.

*Data & Methods:*

Using the [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1), we searched final rules from the beginning of each president’s first term for keywords that indicate a rule’s effective date or compliance date was delayed. Specifically, if a rule contained the words "delay" and either "effective date" or "compliance date," we flagged it as a regulatory suspension. Searching the full text of documents proved to be overly inclusive (i.e., picking up many false positives), so instead we focused on searching three particular fields from the Federal Register API -- *title*, *action*, and *dates* -- for those terms. We limited our timeframe to roughly the first 100 days of each president’s first term -- January 20 to April 30 -- because this would capture a substantial chunk of the initial regulatory activity of a new administration and ensured that we had enough data for Joe Biden’s first year in office. Since document-level data from the Federal Register only date back to 1994, we stop our search for regulatory suspensions at the George W. Bush administration.

We conducted three robustness checks to verify the accuracy of our search method for regulatory suspensions. First, we sampled 50 percent of the identified suspensions from each president (115 out of 227 rules), which had an accuracy rate of 95.7 percent (110/115 with 5 false positives). Second, we sampled 5 percent of the total rules published in the time period from each president (171 out of 3375 rules), producing an accuracy rate of 97.7 percent (167/171 with 1 false positive and 3 false negatives). Third, we sampled 5 percent of the rules from each President identified as non-suspensions via the search method (159 out of 3148 rules). The accuracy rate was 99.4 percent (158/159 with 1 false negative). Each check had an accuracy rate greater than 95 percent, suggesting that our method is sufficiently accurate to reliably establish the broader trends and magnitudes of how presidents use regulatory suspensions.

While conducting accuracy checks, we noticed that some regulatory actions delayed the effective date for multiple rules. In the *action* and *dates* columns, the multiple-rule suspensions would typically say "delay of effective dates" rather than "delay of effective date," as well as refer to "each regulation." To identify multiple-rule suspensions, we searched the 227 regulatory actions containing suspensions using a regex search for "\bdates\b|\beach\b" (i.e., "dates" or "each" with word boundaries at the beginning and end) in either the *dates* or *action* columns. We manually read the flagged regulatory actions, determined how many suspensions each included, and revised the data accordingly.

*Repository Contents:*

The subfolder *Data - Federal Register API* contains Python code to retrieve the raw data from the Federal Register and conduct some initial processing. Specifically, the files: 
- retrieve the population of rules published at the beginning of each presidential administration (January 20 to April 30)
- identify and filter out rules issued by the outgoing president that were published on or after January 20
- retrieve the population of midnight rules published at the end of the previous presidential administration (election day to inauguration day)
- export the data on midnight rules for each president

The subfolder *Method - Identifying rules* contains Python and R code for identifying regulatory suspensions from the population of regulations. Specifically, the files:
- provide one method for identifying regulatory suspensions
- provide a second method for identifying regulatory suspensions (with identical results)
- identify and count the number of midnight rules for each presidential administration
- identifying actions that contain multiple-rule suspensions

The subfolder *Method - Robustness checks* contains R code for conducting accuracy checks on the method for identifying regulatory suspensions. Specifically, the files:
- sample 5 percent of the total rules published in the time period from each president (171 out of 3375 rules) 
- sample 50 percent of the identified suspensions from each president (115 out of 227 rules)
- sample 5 percent of the rules from each President identified as non-suspensions via the search method (159 out of 3148 rules)
- calculate the accuracy rate for each sample

The subfolder *Data - for analysis* contains data produced for analysis. Specifically, the files:
- provide text descriptions for each file
- list the rules issued in the first 100 days of each administration
- list the rules containing regulatory suspensions in the first 100 days of each administration
- list the midnight rules issued between election day and inauguration day at the end of the prior administration
- provide the samples used in the subfolder *Method - Robustness checks*


**--------------**

*Contributors:* Mark Febrizio & Kekai Liu

Please reach out to Mark with any questions: mfebrizio at gwu dot edu
