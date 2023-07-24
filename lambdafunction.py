import os
import logging
import ask_sdk_core.utils as ask_utils
import boto3
import random
from datetime import datetime, timedelta
import pytz

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

scope = ["https://www.googleapis.com/auth/calendar"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
API_NAME = 'calendar'
API_VERSION = 'v3'

# google calendar service
service = build(API_NAME, API_VERSION, credentials=creds)


dynamodb = boto3.resource('dynamodb')
table_name1 = "Patient_Registration"
table = dynamodb.Table(table_name1)

def convert_email(email):
    converted_email = email.replace(" dot ", ".").replace(" at ", "@").replace(" ", "").lower()
    return converted_email


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome to XYZ Hospital Registration. Are you a new patient or a returning patient?"
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response




class NewPatientIntentHandler(AbstractRequestHandler):
    """Handler for NewPatientIntent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NewPatientIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Thank you for choosing XYZ Hospital. Please provide your information. What is your full name? To say your name say My name is"
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

import random
import boto3

class GatherUserInfoIntentHandler(AbstractRequestHandler):
    """Handler for GatherUserInfoIntent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GatherUserInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots

        patient_name = slots['FullName'].value
        age = slots['Age'].value
        # Get the main value of the gender slot
        gender_slot = slots['Gender']
        gender = gender_slot.resolutions.resolutions_per_authority[0].values[0].value.name
        DOB = slots["DOB"].value
        Father_name = slots["Father_name"].value
        email = slots['Email'].value
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['patient_name'] = patient_name
        session_attr['age'] = age
        session_attr['gender'] = gender
        session_attr['DOB'] = DOB
        session_attr['Father_name'] = Father_name
        
        
        email = email.lower()
        email = email.replace(" at ", "@").replace(" dot ", ".").replace(" ","")
        session_attr['email'] = email
        ses_client = boto3.client('ses', region_name="eu-north-1")
        response = ses_client.list_identities(IdentityType='EmailAddress')
        verified_emails = response['Identities']

        if email not in verified_emails:
            # Email not verified, send verification email
            verify_email_identity(email)
            
            speak_output = f"Thank you for providing your information. A verification email has been sent to your email address. Please check your inbox and follow the instructions to verify your email. Once you have verified your email, say 'Verified'."
        else:
            # Email already verified, generate user ID and send user information
            # Generate a new patient ID
            patient_id = str(random.randint(10000000, 99999999))
            session_attr['patient_id'] = patient_id
            store_user_info(patient_id, patient_name, age, gender,DOB, Father_name, email)
            send_email(email, patient_name, patient_id)
            speak_output = f"Thank you for providing your information. Your ID is {patient_id}. The details have been sent to the email.How may I assist you today? If you want to schedule an appointment, Please say Schedule an appointment."
    
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
def verify_email_identity(email):
    ses_client = boto3.client('ses', region_name="eu-north-1")
    response = ses_client.verify_email_identity(EmailAddress=email)
    return response
    
    
class VerifyEmailIntentHandler(AbstractRequestHandler):
    """Handler for the 'VerifyEmailIntent' to handle user confirmation of email verification."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("VerifyEmailIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        email = session_attr.get('email')
        patient_name = session_attr.get('patient_name')
        age = session_attr.get('age')
        gender = session_attr.get('gender')
        DOB = session_attr.get('DOB')
        Father_name = session_attr.get('Father_name')

        # Generate a new patient ID
        patient_id = str(random.randint(10000000, 99999999))
        session_attr['patient_id'] = patient_id
        store_user_info(patient_id, patient_name, age, gender, DOB, Father_name, email)
        send_email(email, patient_name, patient_id)
        speak_output = f"Thank you for verifying your email. Your ID is {patient_id}.The details have been sent to your email. If you want to schedule an appointment, Please say Schedule an appointment."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

def store_user_info(id, name, age, gender, DOB, Father_name, email):
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='Patient_Registration',
        Item={
            'patient_id': {'S': id},
            'full_name': {'S': name},
            'age': {'N': str(age)},
            'gender': {'S': gender},
            'DOB': {'S': DOB},
            'Father_name': {'S': Father_name},
            'email': {'S': email}
        }
    )


def send_email(email, name, user_id):
    ses_client = boto3.client('ses',region_name="eu-north-1")
    sender_email = "apollohospitals553@gmail.com" 
    subject = "Your Details are stored"
    body = f"Mr/Mrs.{name},your information has been stored. Your ID is {user_id}."
    
    response = ses_client.send_email(
        Source=sender_email,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    return response



class ReturningPatientIntentHandler(AbstractRequestHandler):
    """Handler for ReturningPatientIntent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ReturningPatientIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        patient_id = slots["PatientID"].value

        if not patient_id:
            speak_output = "Please provide your patient ID."
        else:
            dynamodb = boto3.resource('dynamodb')
            table_name1 = "Patient_Registration"
            table = dynamodb.Table(table_name1)

            response = table.get_item(Key={'patient_id': patient_id})
            if 'Item' in response:
                patient = response['Item']
                patient_name = patient['full_name']
                email = patient['email']
                speak_output = f"Welcome back! {patient_name} How may I assist you today? If you want to schedule an appointment, Please say Schedule an appointment."
                handler_input.attributes_manager.session_attributes['patient_id'] = patient_id
                handler_input.attributes_manager.session_attributes['patient_name'] = patient_name
                handler_input.attributes_manager.session_attributes['email'] = email
    
            else:
                speak_output = "I'm sorry to hear that you forgot your patient ID. " \
                                "May I please ask your father's name in order to verify your identity as our patient?"
                                
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response
  
from boto3.dynamodb.conditions import Key, Attr      

class ForgotPasswordIntentHandler(AbstractRequestHandler):
    """Handler for ForgotPasswordIntent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ForgotPasswordIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        Father_name = slots["FatherName"].value
        father_name = Father_name
        if not father_name:
            speak_output = "Please provide your father's name."
        else:
            # Query the database for patient ID based on father's name
            dynamodb = boto3.resource('dynamodb')
            table_name = "Patient_Registration"
            table = dynamodb.Table(table_name)

            response = table.scan(
                FilterExpression=Attr('Father_name').eq(father_name)
            )
            items = response.get('Items', [])

            if len(items) > 0:
                patient_id = items[0]['patient_id']
                dynamodb = boto3.resource('dynamodb')
                table_name1 = "Patient_Registration"
                table = dynamodb.Table(table_name1)
    
                response = table.get_item(Key={'patient_id': patient_id})
                if 'Item' in response:
                    patient = response['Item']
                    patient_name = patient['full_name']
                    handler_input.attributes_manager.session_attributes['patient_id'] = patient_id
                    handler_input.attributes_manager.session_attributes['patient_name'] = patient_name
    
                    speak_output = f"Welcome back! {patient_name}. Your Patient ID is {patient_id}. Please remember it for future assistance. How may I assist you today? If you want to schedule an appointment, Please say Schedule an appointment."
                    handler_input.attributes_manager.session_attributes['patient_id'] = patient_id
            else:
                speak_output = f"There is no patient with the father's name {father_name}. Please check the name or register as a new patient."
      

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

        
class ScheduleIntentHandler(AbstractRequestHandler):
    """Handler for ScheduleIntent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ScheduleIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        date = str(slots["date"].value)
        time = str(slots["time"].value)
        specialization = str(slots["specialization"].value)
        date_slot = datetime.strptime(date, "%Y-%m-%d")
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        time_min = datetime(date_slot.year, date_slot.month, date_slot.day, hour, mins)
        time_max = time_min + timedelta(hours=1)

        if not specialization:
            speak_output = "Please provide the specialization."
        elif not date:
            speak_output = "Please provide the date for the appointment."
        elif not time:
            speak_output = "Please provide the time for the appointment."
        else:
            # Check doctor's availability for the given specialization
            available_doctors, calendar_ids = check_doctor_availability_for_specialization(specialization, time_min, time_max)
            if available_doctors:
                speak_output = "The following doctors are available for the provided specialization, date, and time:\n"
                for i, (doctor_name) in enumerate(available_doctors, 1):
                    speak_output += f"{i}. Dr. {doctor_name} , \n"
                speak_output += "Please choose a doctor from the list to schedule an appointment. To choose, say Schedule appointment with choosen doctor name."
            else:
                speak_output = "There are no available doctors for the provided specialization, date, and time."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)  # Asking the user to choose a doctor
            .response
        )


def check_doctor_availability_for_specialization(specialization, time_min, time_max):
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name2 = "doctor_calendar_table"
        table2 = dynamodb.Table(table_name2)

        response = table2.scan(
            FilterExpression='specialization = :s',
            ExpressionAttributeValues={':s': specialization}
        )

        doctors = response.get('Items', [])
        available_doctors = []
        calendar_ids = []  # Store doctor_calendar_ids

        for doctor in doctors:
            doctor_name = doctor['doctor_name']
            doctor_calendar_id = doctor['calendar_id']
            calendar_ids.append(doctor_calendar_id)  # Add calendar_id to the list
            if check_doctor_availability(doctor_calendar_id, time_min, time_max):
                
                available_doctors.append(doctor_name)

        if available_doctors:
            return available_doctors, calendar_ids  # Return available doctors and calendar_ids
        else:
            return [], calendar_ids  # Return empty list for both

    except Exception as e:
        logging.error(f"Error checking doctor availability for specialization: {str(e)}")
        return [], calendar_ids  # Return empty lists including calendar_ids in case of an error



class ScheduleWithDoctorIntentHandler(AbstractRequestHandler):
    """Handler for ScheduleWithDoctorIntent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ScheduleWithDoctorIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        doctName = slots["doctName"].value
        doctor_name = doctName.lower()
        print(doctor_name)
        session_attr = handler_input.attributes_manager.session_attributes
        email = session_attr.get('email')
        # Retrieve the calendar ID from the DynamoDB table based on the doctor's name
        calendar_id = get_calendar_id_by_doctor_name(doctor_name)
        #speak_output=" calendar{calendar_id} docName{doctName}"
        date = slots["date"].value
        time = slots["time"].value
        dateSlot = datetime.strptime(date, "%Y-%m-%d")
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        time_min = datetime(dateSlot.year, dateSlot.month, dateSlot.day, hour, mins)
        time_max = time_min + timedelta(hours=1)
        # Store the time_min value in session attributes
        handler_input.attributes_manager.session_attributes["time_min"] = str(time_min)
        if check_free_busy(time_min, time_max,calendar_id):
            reserve_appointment(handler_input, time_min, time_max, calendar_id)
            speak_output = f"Your appointment with Dr.{doctName} on {date} at {time} is successfully scheduled."
            send_email_scheduled(email, doctName, date, time)
        else :
            speak_output = f"Sorry, the selected time is not available. Would you like to schedule in the next available slot?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Please confirm if you want to book the next available slot.")  # Ask for confirmation
                .response
        )
        
def send_email_scheduled(email, name, date, time):
    ses_client = boto3.client('ses', region_name="eu-north-1")
    sender_email = "apollohospitals553@gmail.com"
    subject = "Appointment Scheduled!!"
    body = f"Your appointment with Dr.{name} on {date} at {time} is successfully scheduled."

    response = ses_client.send_email(
        Source=sender_email,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    return response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for HelpIntent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can say whether you are a new patient or a returning patient. " \
                       "If you are a new patient, provide your information when prompted. " \
                       "If you are a returning patient, provide your patient ID when prompted."
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class ExitIntentHandler(AbstractRequestHandler):
    """Handler for Cancel, Stop, and NoIntent."""
    def can_handle(self, handler_input):
        return (
            ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
            or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
            or ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)
        )

    def handle(self, handler_input):
        speak_output = "Thank you for using XYZ Hospital Registration. Goodbye!"
        return handler_input.response_builder.speak(speak_output).response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for FallbackIntent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Sorry, I didn't understand that. Please try again."
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Handler for all exception types."""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speak_output = "Sorry, there was a problem. Please try again!"
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


# Skill Builder object
sb = SkillBuilder()

# Add all request handlers to the skill builder
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ReturningPatientIntentHandler())
sb.add_request_handler(NewPatientIntentHandler())
sb.add_request_handler(GatherUserInfoIntentHandler())
sb.add_request_handler(ForgotPasswordIntentHandler())
sb.add_request_handler(ScheduleIntentHandler())
sb.add_request_handler(ScheduleWithDoctorIntentHandler())
sb.add_request_handler(VerifyEmailIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(FallbackIntentHandler())

# Add exception handler to the skill builder
sb.add_exception_handler(CatchAllExceptionHandler())

# Lambda handler function
lambda_handler = sb.lambda_handler()


def reserve_appointment(handler_input, time_min, time_max, calendar_id):
    patient_id = handler_input.attributes_manager.session_attributes.get("patient_id")
    patient_name = handler_input.attributes_manager.session_attributes.get("patient_name")
    
    timezone = pytz.timezone('Asia/Kolkata')
    time_min_ist = time_min.astimezone(timezone)
    time_max_ist = time_max.astimezone(timezone)
    event = {
        'summary': 'appointment',
        'description': f"PatientID of patient:{patient_id} \nPatient name: {patient_name}",
        'start': {
            'dateTime': time_min_ist.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': time_max_ist.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }
    response = service.events().insert(calendarId=calendar_id, body=event).execute()


import logging
import pytz
from datetime import datetime

def check_free_busy(time_min, time_max,calendar_id):
    try:
        ist_timezone = pytz.timezone('Asia/Kolkata')
        time_min_ist = time_min.astimezone(ist_timezone)
        time_max_ist = time_max.astimezone(ist_timezone)
        free_busy_query = {
            'timeMin': time_min_ist.isoformat(),
            'timeMax': time_max_ist.isoformat(),
            'timeZone': 'Asia/Kolkata',
            'items': [{'id': calendar_id}]
        }
        free_busy_result = service.freebusy().query(body=free_busy_query).execute()
        is_busy = False
        for cal, busy_list in free_busy_result['calendars'].items():
            if busy_list['busy']:
                is_busy = True
                break
        return not is_busy
    except Exception as e:
        logger.error(e, exc_info=True)
        return False



def check_doctor_availability(calendar_id, time_min=None, time_max=None):
    try:
        if not time_min or not time_max:
            # If time_min and time_max are not provided, check for general availability of the doctor
            # without specifying a specific time slot
            time_min = datetime.now() + timedelta(minutes=1)
            time_max = datetime.now() + timedelta(days=7)

        # Convert time_min and time_max to IST timezone
        ist_timezone = pytz.timezone('Asia/Kolkata')
        time_min_ist = time_min.astimezone(ist_timezone)
        time_max_ist = time_max.astimezone(ist_timezone)

        # Check the doctor's calendar for availability within the specified time slot
        response = service.freebusy().query(
            body={
                'timeMin': time_min_ist.isoformat(),
                'timeMax': time_max_ist.isoformat(),
                'timeZone': 'Asia/Kolkata',
                'items': [{'id': calendar_id}]
            }
        ).execute()
        
        calendars = response.get('calendars', {})
        doctor_calendar = calendars.get(calendar_id, {})
        busy_slots = doctor_calendar.get('busy', [])
        
        return len(busy_slots) == 0
    except Exception as e:
        logging.error(f"Error checking doctor's availability: {str(e)}")
        return False
        
        
def get_calendar_id_by_doctor_name(doctName):
    # Initialize the DynamoDB client
    dynamodb = boto3.client('dynamodb')
    
    response = dynamodb.scan(
        TableName='doctor_calendar_table',
        FilterExpression='doctor_name = :name',
        ExpressionAttributeValues={
            ':name': {'S': doctName}
        }
    )
    
    # Check if a matching record was found
    if response['Count'] > 0:
        item = response['Items'][0]
        calendar_id = item['calendar_id']['S']
        return calendar_id
    
    return None