import requests
from bs4 import BeautifulSoup
base_url = "https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{}.htm"
state_codes_Union_codes = ['S24', 'S01', 'S02', 'S03','U05','S10','S12','S21','S14','U09','U08'] 

url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"


total_party_votes = {}
max_votes_s24 = 0    
max_party_s24 = ''
max_votes_U05 = 0    
max_party_U05 = '' 
max_votes_S10 = 0
max_party_S10 = ''  
max_votes_S12 = 0
max_party_S12 = ''
max_votes_S21 = 0
max_party_S21 = ''
max_votes_S14 = 0
max_party_S14 = ''
max_votes_U09 = 0
max_party_U09 = ''
max_votes_U08 = 0
max_party_U08 = ''


response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'class': 'table'})
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if len(columns) > 1:
        party_name = columns[0].get_text(strip=True)
        votes = int(columns[1].get_text(strip=True).replace(',', ''))
        
        if party_name in total_party_votes:
            total_party_votes[party_name] += votes
        else:
            total_party_votes[party_name] = votes
for state_code in state_codes_Union_codes:
    url = base_url.format(state_code)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'table'})
    if not table:
        continue
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 1:
            party_name = columns[0].get_text(strip=True)
            votes = int(columns[1].get_text(strip=True).replace(',', ''))
            if state_code == 'S24' and votes > max_votes_s24:
                max_votes_s24 = votes
                max_party_s24 = party_name
            
            if state_code == 'U05' and votes > max_votes_U05:
                max_votes_U05 = votes
                max_party_U05 = party_name

            if state_code =='S10' and votes >max_votes_S10:
                max_votes_S10 = votes
                max_party_S10 = party_name
            if state_code =='S12' and votes > max_votes_S12:
                max_votes_S12 = votes
                max_party_S12 = party_name
            if state_code =='S21' and votes > max_votes_S21:
                max_votes_S21 = votes
                max_party_S21 = party_name
            
            if state_code =='S14' and votes > max_votes_S14:
                max_votes_S14 = votes
                max_party_S14 = party_name
            if state_code =='U09' and votes > max_votes_U09:
                max_votes_U09 = votes
                max_party_U09 = party_name
            if state_code =='U08' and votes > max_votes_U08:
                max_votes_U08 = votes
                max_party_U08 = party_name

max_votes_party = max(total_party_votes, key=total_party_votes.get)
min_votes_party = min(total_party_votes, key=total_party_votes.get)




html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Election Results Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ text-align: center; }}
        .section {{ margin: 20px 0; }}
        .section h2 {{ margin-bottom: 10px; }}
        .section p {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h1>Election Results Report</h1>
    
    <div class="section">
        <h2>Overall Results:</h2>
        <p><strong>Winning Party and the Party with the maximum votes across all constituencies:</strong> {max_votes_party} ({total_party_votes[max_votes_party]} votes but has has lost 63 constituencies compared to its 2019 elections)</p>
        <p><strong>Party with the least votes across all constituencies:</strong> {min_votes_party} ({total_party_votes[min_votes_party]} constituencies)</p>
        <h3><strong>Insights Related to States and Union Territories</strong></h3>
        <p><strong>In Uttar Pradesh, the party with the maximum votes is</strong> {max_party_s24} with winning {max_votes_s24}  constituencies. )</p>
        <p><strong>In Delhi, the party with the maximum votes is</strong> {max_party_U05} with winning {max_votes_U05} constituencies. )</p>
        <p><strong>In Karnataka , the party with the maximum votes is</strong> {max_party_S10} with {max_votes_S10} constituencies and Janta Dal Looses becuase of Prajwal Rewanna Sex Scandal )</p>
        <p><strong>In Madhya Pradesh , all the constituencies were won by a single party which is </strong> {max_party_S12} with {max_votes_S12}  )</p>
        <p><strong>In Sikkim there was only a single constituency and also only a single party standing for election which was </strong> {max_party_S21} and won {max_votes_S21}  constituencies )</p>
        <p><strong>In Manipur BJP lost and  </strong> {max_party_S14} has won {max_votes_S14}  all constituencies becuase of manipur tribal fights)</p>
        <p><strong>In Ladakh no party has won but an independent person has won </strong> {max_party_U09} has won {max_votes_U09} all constituencies)</p>
        <p><strong>In Jammu & Kashmir there is and tie between two parties </strong> {max_party_U08}  and Bharatiya Janata Party who  has won {max_votes_U08}  constituencies)</p>
    </div>

    
</body>
</html>
"""
with open("election_results_report.html", "w") as file:
    file.write(html_report)

