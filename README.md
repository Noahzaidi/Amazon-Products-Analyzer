# Amazon-Products-Analyzer
Amazon FBA GUI App. Imports &amp; enrichs Jungle Scout CSV data, calculates insights like competitor count, sales, reviews. Metrics include unique competitors, zero-sales products, new entries, LQS, brands, top/bottom competitor performance, average rank, fees, and revenue trends.

GUI App to analyze Amazon products FBA (Fulfillment by Amazon) in Jungle Scout CSV format. 

The application allows users to import product data from an Excel file, add additional data to the existing dataset, and analyze the data to obtain various metrics and insights.

Importing Excel File: Users can select an Excel file containing product data to import into the application.

Adding Data: Users can add additional data from another Excel file to the existing dataset.

Validating and Analyzing Data: Users can validate the data and perform analysis on the dataset to obtain various metrics such as the number of competitors, average market sales, average price, average reviews, etc.

Displaying Analysis Results: The application displays the analysis results in a table format and provides a summary of the metrics calculated. All these Data (Insights include could be exported in excel format).

Apart of the calculated metrics of input data , there´s 4 more relevant statistical insights also calculated in the table widgets that are the POS index (the quality of the listing), CI  index (Competition index), the pi is the multiplication of 0.5 by the ci + 0.5 by the pos, because both are equally important, but it can be changed to 0.7 0.3, or 0.4 0.6, depending on whether we consider that competition or the quality of the listing has more weight in the market, and the lastly a success rate index.

The POS formula uses the following product information:

LQS: Listing Quality Score, which is a quality metric of the product's listing on Amazon.
Reviews: The number of reviews for the product.
Rating: The average rating of the product.
Est. Monthly Sales: The estimated monthly sales of the product.
Date First Available: The date the product was first available on Amazon.
The formula to calculate POS is:

pos = lqs_score * reviews_score * rating_score * sales_velocity_score

Where:

lqs_score is LQS normalized to the range [0, 1] divided by 10.
reviews_score is 1 minus the ratio of product reviews to total reviews (reviews / (reviews + 1)).
rating_score is the product rating normalized to the range [0, 1] divided by 5.
sales_velocity is the ratio of estimated monthly sales to the number of days since the product was first available on Amazon.
sales_velocity_score is the ratio of sales_velocity to total sales (sales_velocity / (sales_velocity + 1)).
The function returns the calculated POS value. This value can be used to assess the potential of a product on the Amazon FBA marketplace in terms of its listing quality, reviews, rating, and sales velocity.


The calculate_ci method is a function defined in the ProductAnalyzer class, and calculates the Competition Index (CI) of a given product in a DataFrame. The function takes as arguments the DataFrame df and an index corresponding to the row of the product for which the CI will be calculated. Here is a step-by-step description of how CI is calculated:

Gets the product row in the DataFrame using the provided index.
Calculates rank_score as 1 - (row['Rank'] / (row['Rank'] + 1)).
Calculates sellers_score as 1 - (row['Sellers'] / (row['Sellers'] + 1)).
Calculates price_var_score as 1 - abs(row['Price'] - df['Price'].mean()) / df['Price'].std().
Finally, it calculates the CI as the product of rank_score, sellers_score, and price_var_score.
The competition index (CI) is a measure of how a product performs compared to its competitors in terms of range, number of sellers, and price variance. A higher CI indicates greater competitiveness in the market.

In summary, the calculate_ci function calculates a product's competition index using the product's rank, number of sellers, and price variance relative to the mean and standard deviation of the prices of all products in the DataFrame.

calculate_success_index is not exactly a "success rate" but rather a "success index" that represents how well a particular product performs compared to other products in the data set, considering multiple factors. The function takes a row of the DataFrame (representing a product) as an argument and calculates its success rate using the following logic:

Initializes the success rate to 0.
Iterates through the factor weights predefined in the self.weights dictionary. The factors included in this example are: 'Price', 'LQS', 'Est. Monthly Sales', 'Est. Monthly Revenue', 'Reviews'.
For each factor and its weight, calculates the relative difference between the factor value for the current product (in the row) and the mean value of that factor across the entire data set. Divide the absolute difference by the standard deviation of the factor in the data set.
Multiply the relative difference by the factor weight and add the result to the success rate.
Once all factors have been considered, return the final success rate.
The success rate is used to compare the performance of the products in the dataset and analyze how a particular product performs compared to others in terms of key factors such as price, estimated monthly sales, estimated monthly revenue, number of reviews, and LQS (Listing Quality Score).




The metrics are the following :

Number of Records: This metric represents the total number of product records in the dataset. It gives an overview of the size of the dataset.

Number of Competitors: This metric indicates the number of unique competitors in the dataset. It helps to understand the level of competition in the market.

Competitors with Zero Sales: This metric counts the number of competitors with zero monthly sales. It provides insights into the presence of products that are not generating any sales.

Competitors with Sales Greater than Zero: This metric counts the number of competitors with monthly sales greater than zero. It highlights the number of active products with sales activity.

New Competitors (Current Year): This metric calculates the number of new competitors that entered the market in the current year. It gives insights into the level of competition and market dynamics.

Average Market Sales: This metric represents the average monthly sales of all products in the dataset. It provides a benchmark for evaluating individual product sales.

Most Used Price: This metric identifies the price value that appears most frequently in the dataset. It helps to identify the commonly used price point among competitors.

Average Price: This metric calculates the average price of all products in the dataset. It provides an overview of the pricing landscape in the market.

Average LQS (Listing Quality Score): LQS is a metric that measures the quality of a product listing on Amazon. This metric calculates the average LQS value among all competitors. A higher LQS indicates better listing quality.

Number of Brands: This metric counts the number of unique brands among the competitors. It helps to understand the diversity of brands in the market.

Average Reviews: This metric calculates the average number of reviews across all products in the dataset. It provides insights into the average customer feedback and product ratings.

Average Reviews of Top 10 Selling Competitors: This metric calculates the average number of reviews among the top 10 selling competitors. It helps to identify the average customer engagement and satisfaction among the most successful products.

Average Sales of Top 10 Selling Competitors: This metric calculates the average monthly sales among the top 10 selling competitors. It gives insights into the sales performance of the most successful products.

Average Reviews of Bottom 10 Selling Competitors: This metric calculates the average number of reviews among the bottom 10 selling competitors. It helps to identify the average customer engagement and satisfaction among the least successful products.

Average Sales of Bottom 10 Selling Competitors: This metric calculates the average monthly sales among the bottom 10 selling competitors. It gives insights into the sales performance of the least successful products.

Average Rank: This metric calculates the average rank of all products in the dataset. It provides an indication of the competitive positioning of products.

Average Fees: This metric calculates the average fees associated with the products in the dataset. It helps to understand the cost structure and profitability.

Most Repeated Word: This metric identifies the most frequently occurring word in the product names. It gives insights into common themes or keywords used by competitors.

Average Revenue: This metric calculates the average monthly revenue across all products in the dataset. It provides an overview of the revenue potential in the market.

Proportional Mean Sales: This metric calculates the weighted average of monthly sales based on the revenue contribution of each product. It provides a more accurate representation of the market's sales distribution.

Proportional Mean Price: This metric calculates the weighted average of product prices based on the revenue contribution of each product. It helps to understand the average price point considering the revenue distribution.

These metrics and insights enable users to assess market trends, competition levels, pricing strategies, customer feedback, and overall market performance. They assist in making informed decisions for product selection, pricing, and marketing strategies in the Amazon FBA ecosystem.
