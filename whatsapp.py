from twilio.rest import Client
import streamlit as st
import openai
import pandas as pd
from datetime import datetime, timedelta


from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse


# Initialize the Twilio client with your Twilio credentials
twilio_account_sid = "ACa3ce04ad51439fbcda4911c9dedea089"
twilio_auth_token = "f0a603f56b9d01e1d53ca8351603062c"
twilio_phone_number = "whatsapp:+14155238886"
client = Client(twilio_account_sid, twilio_auth_token)

# Set your OpenAI API key
openai.api_key = "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"


# Load your marketing data
data = pd.read_csv("marketing_dataset.csv")
data.drop(columns='Unnamed: 0', inplace=True)
data.Date = pd.to_datetime(data.Date)

# Function to calculate date ranges based on user input
def calculate_date_range(user_input):
    words = user_input.split()
    today = datetime.today().date()
    start_date = None
    end_date = None
    
    for i in range(len(words)):
        if (words[i] == "last" or words[i] == "past") and i + 1 <= len(words):
            if words[i + 1] == "month":
                # Calculate start and end dates for the last month
                start_date = (today - timedelta(days=today.day)).replace(day=1)
                end_date = today - timedelta(days=today.day)
                break
            elif words[i + 1] == "week":
                # Calculate start and end dates for the last week
                start_date = today - timedelta(days=today.weekday() + 6)
                end_date = today - timedelta(days=today.weekday())
                break
            elif words[i + 1].isdigit() and words[i + 2] == "days":
                # Calculate start and end dates for specified number of days
                num_days = int(words[i + 1])
                start_date = today - timedelta(days=num_days - 1)
                end_date = today
                break
            break
        
        elif words[i] == "yesterday":
            # Calculate start and end dates for yesterday
            start_date = today - timedelta(days=1)
            end_date = today 
            break 
            # Add more cases for other timeframes
        elif words[i].lower() in ["january", "february", "march", "april", "may", "june",
                                  "july", "august", "september", "october", "november", "december"]:
            # Handle specific month and year input, e.g., "July 2023"
            month = words[i]
            year = words[i + 1]
            start_date = datetime.strptime(f"{month} {year}", "%B %Y").replace(day=1).date()
            end_date = (start_date.replace(month=start_date.month % 12 + 1) - timedelta(days=1))
            break
            
    if start_date is None or end_date is None:
        # If no specific timeframe is identified, default to the last 30 days
        start_date = today - timedelta(days=30)
        end_date = today - timedelta(days=1)
    
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")



# Function to interact with the chatbot and fetch data from the DataFrame
def chat_with_bot(user_input):
    # Process user input to extract relevant information
    # user_input = user_input.lower()
    
    # Split user input to extract metric
    words = user_input.split()
    for i in range(len(words)):
        if words[i] in data.columns:
            metric = words[i]
    
    # Calculate the date range based on user input
    start_date, end_date = calculate_date_range(user_input)
    
    # Filter the DataFrame based on the calculated date range
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    
    
    if any(substring in user_input for substring in data.Platform.unique()):
        for i in range(len(words)):
            if words[i] in data.Platform.unique():
                platform = words[i]
                platform_data = filtered_data.loc[filtered_data.Platform == platform]
                metric_value = platform_data[metric].sum()
                print('platform')
                break
    elif any(substring in user_input for substring in data.Sentiment.unique()):
        for i in range(len(words)):
            if words[i] in data.Sentiment.unique():
                sentiment = words[i]
                sentiment_data = filtered_data.loc[filtered_data.Sentiment == sentiment]
                metric_value = sentiment_data[metric].sum()
                print('Sentiment')
                break
    elif any(substring in user_input for substring in data['Post Type'].unique()):
        for i in range(len(words)):
            if words[i] in data['Post Type'].unique():
                post_type = words[i]
                post_type_data = filtered_data.loc[filtered_data['Post Type'] == post_type]
                metric_value = post_type_data[metric].sum()
                print('Post Type')
                break
        
    elif any(substring in user_input for substring in data.Gender.unique()):
        for i in range(len(words)):
            if words[i] in data.Gender.unique():
                gender = words[i]
                gender_data = filtered_data.loc[filtered_data.Gender == gender]
                metric_value = gender_data[metric].sum()
                print('Gender')
                break
        
    elif any(substring in user_input for substring in data.Age.unique()):
        for i in range(len(words)):
            if words[i] in data.Age.unique():
                age = words[i]
                age_data = filtered_data.loc[filtered_data.Age == age]
                metric_value = age_data[metric].sum()
                print('Age')
                break
        
    elif any(substring in user_input for substring in data.Campaigns.unique()):
        for i in range(len(words)):
            if words[i] in data.Campaigns.unique():
                campaign = words[i]
                campaign_data = filtered_data.loc[filtered_data.Campaigns == campaign]
                metric_value = campaign_data[metric].sum()
                print('Campaigns')
                break
        
    elif any(substring in user_input for substring in data['Campaign Objective'].unique()):
        for i in range(len(words)):
            if words[i] in data['Campaign Objective'].unique():
                campaign_objective = words[i]
                campaign_objective_data = filtered_data.loc[filtered_data['Campaign Objective'] == campaign_objective]
                metric_value = campaign_objective_data[metric].sum()
                print('Campaign Objective')
                break
    
    elif any(substring in user_input for substring in data['Ad Type'].unique()):
        for i in range(len(words)):
            if words[i] in data['Ad Type'].unique():
                ad_type = words[i]
                ad_type_data = filtered_data.loc[filtered_data['Ad Type'] == ad_type]
                metric_value = ad_type_data[metric].sum()
                print('Ad Type')
                break
        
    elif any(substring in user_input for substring in data['Ad Placement'].unique()):
        for i in range(len(words)):
            if words[i] in data['Ad Placement'].unique():
                ad_placement = words[i]
                ad_placement_data = filtered_data.loc[filtered_data['Ad Placement'] == ad_placement]
                metric_value = ad_placement_data[metric].sum()
                print('Ad Placement')
                break
            
    elif any(substring in user_input for substring in data.Locations.unique()):
        for i in range(len(words)):
            if words[i] in data.Locations.unique():
                locations = words[i]
                locations_data = filtered_data.loc[filtered_data.Locations == locations]
                metric_value = locations_data[metric].sum()
                print('Locations')
                break
    
    else:
        # Get the relevant metric value from the filtered data
        metric_value = filtered_data[metric].sum()
        print('nopatform')
            
    
    # Generate a response using the metric value and the OpenAI model
    bot_response = "The total {} from {} to {} is ${:.2f}".format(
        metric, start_date, end_date, metric_value)
    
    return bot_response



"""
This falsk code started
"""

@app.post("/twilio-webhook")
async def twilio_webhook(request: Request):
    form = await request.form()
    incoming_message = form['Body']
    sender_phone_number = form['From']

    response = process_incoming_message(incoming_message)

    send_whatsapp_message(response, sender_phone_number)

    return "Message received and processed."

def process_incoming_message(incoming_message):
    # Process the incoming message and generate a response
    response = chat_with_bot(incoming_message)
    return response

def send_whatsapp_message(message, target_phone_number):
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=target_phone_number
    )



"""
This is flask code ended
"""

def main():
    st.title("Elisa: Marketing Data Chatbot")
    
    st.markdown("## Hi there! How can I assist you?")
    st.write("Please provide a metric (e.g., clicks, revenue) and other information for your query.")

    user_input = st.text_input("You:")

    if user_input.lower() == "exit" or user_input.lower() == "thank you" or user_input.lower() == "thanks":
        st.markdown("Elisa: Goodbye!")
        return

    metric = None
    words = user_input.split()
    for word in words:
        if word in data.columns:
            metric = word
            break

    if metric is None:
        return

    bot_response = chat_with_bot(user_input)
    st.markdown("Chatbot: **" + bot_response + "**")

    # Send bot response to WhatsApp using Twilio
    send_whatsapp_message(bot_response)

def send_whatsapp_message(message):
    target_phone_number = "whatsapp:+923164735033"
    
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=target_phone_number
    )

if __name__ == "__main__":
    main()
