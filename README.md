# regulatory-suspensions

[Regulatory suspensions](https://www.theregreview.org/2020/03/16/davis-noll-revesz-regulatory-rollbacks-changed-nature-presidential-power/) "defer compliance by either postponing the compliance dates or putting off a regulation’s effective date, prior to working to change or repeal the regulation’s substantive requirements." Suspensions are one of [several mechanisms](https://regulatorystudies.columbian.gwu.edu/biden-using-multiple-mechanisms-reverse-trumps-regulatory-agenda) that incoming presidents use to reverse the regulatory agenda of the prior administration. Federal agencies publish these postponements in the [Federal Register](https://www.federalregister.gov/), the daily journal of the US government. Understanding the frequency of regulatory suspensions across presidential administrations may help contextualize the usage of this tool of regulatory oversight. Our objective is to identify regulatory suspensions and analyze how presidential administrations use them differently.

*Data & Methods*

Using the [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1), we searched final rules from the beginning of each president’s first term for keywords that indicate a rule’s effective date or compliance date was delayed. Specifically, if a rule contained the words “delay” and either “effective date” or “compliance date,” we flagged it as a regulatory suspension. Searching the full text of documents proved to be overly inclusive (i.e., picking up many false positives), so instead we focused on searching three particular fields from the Federal Register API -- title, action, and dates -- for those terms. We limited our timeframe to roughly the first 100 days of each president’s first term -- January 20 to April 30 -- because this would capture a substantial chunk of the initial regulatory activity of a new administration and ensured that we had enough data for Joe Biden’s first year in office. Since document-level data from the Federal Register only date back to 1994, we stop our search for regulatory suspensions at the George W. Bush administration.

We conducted three robustness checks to verify the accuracy of our search method for regulatory suspensions. First, we sampled 50 percent of the identified suspensions from each president (115 out of 227 rules), which had an accuracy rate of 95.7 percent (110/115 with 5 false positives). Second, we sampled 5 percent of the total rules published in the time period from each president (171 out of 3375 rules), producing an accuracy rate of 97.7 percent (167/171 with 1 false positive and 3 false negatives). Third, we sampled 5 percent of the rules from each President identified as non-suspensions via the search method (159 out of 3148 rules). The accuracy rate was 99.4 percent (158/159 with 1 false negative). Each check had an accuracy rate greater than 95 percent, suggesting that our method is sufficiently accurate to reliably establish the broader trends and magnitudes of how presidents use regulatory suspensions. The code for those accuracy checks are located in the XX folder.
