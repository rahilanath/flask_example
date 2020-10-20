# Chinook Database Analysis

* In this activity, you will convert some exploratory analysis of the [chinook](https://chinookdatabase.codeplex.com/wikipage?title=Chinook_Schema&referringTitle=Home) database into a flask api.

## Instructions

* Read through the jupyter notebook to understand the analysis.

* In the `app.py` starter code file add an endpoint for each query in the analysis.

  * Design an endpoint that returns a list of the billing countries found in the invoices table.

  * Design an endpoint that returns the invoices totals for each billing country in a list of dictionaries format.

    * **Hint**: You'll need to convert the Decimal formatted value returned by the query to something that can be jsonified.

  * Design an endpoint that lists all of the Billing Postal Codes for a country.

  * Design an endpoint that returns a dictionary of the inputted country and it's aggregated item totals.

  * Design an endpoint that returns a list of dictionaries of item totals per postal code for an inputted country.

* Build out the root route with a list of links to all the endpoints.