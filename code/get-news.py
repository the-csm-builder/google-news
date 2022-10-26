from datetime import datetime, timezone, timedelta
from newsapi import NewsApiClient
import pandas as pd

today = str(datetime)
newsapi = NewsApiClient(api_key='XXX')
search = 'XXX'

from_date = datetime.now(timezone.utc) + timedelta(days=-7)
end_time = datetime.now(timezone.utc) + timedelta(days=0)

# /v2/everything
all_articles = newsapi.get_everything(q=search,
                                      from_param=from_date,
                                      to=end_time,
                                      language='en',
                                      sort_by='relevancy'
                                      )
# Create Pandas DataFrame
df =pd.DataFrame(all_articles['articles'])
df.sort_values(by=['publishedAt'], ascending=True)
# Save DataFrame to CSV

df.to_csv(str(datetime.now(timezone.utc)) + '-' + search + '-'+'news.csv')