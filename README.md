# Hospital Appointment Scheduler using Alexa 

## Introduction

Step into the world of seamless healthcare management with our cutting-edge Hospital Appointment Scheduler using Alexa skill! Embrace the future of healthcare as you effortlessly book appointments with renowned doctors at XYZ Hospital, all at your command through any Alexa-enabled device. With this skill, you hold the power to manage your health with ease, making the entire appointment booking process a breeze while ensuring you receive the best medical care possible.

## Problem Statement

The primary goal of the Hospital Appointment Scheduler using Alexa skill is to streamline the process of scheduling doctor appointments for patients. The skill aims to provide a seamless and user-friendly interface that allows patients to register, verify their identity, and schedule appointments with their preferred doctors based on availability.

## Solution Overview

The Hospital Appointment Scheduler skill is built using the Alexa Skills Kit (ASK) and integrates with AWS Lambda for serverless execution. It leverages AWS DynamoDB for storing patient and doctor information, Google Calendar API for doctor availability, and Amazon Simple Email Service (SES) for email notifications.

Here's an overview of the key components of the solution:

1. **User Registration and Verification**: New patients can register by providing their information, including full name, age, gender, date of birth (DOB), father's name, and email. The skill sends a verification email to the provided email address for identity confirmation.

2. **Returning Patients**: Returning patients can log in using their patient ID. If they forget their patient ID, they can verify their identity by providing their father's name.

3. **Doctor Availability Checking**: The skill uses the Google Calendar API to check the availability of doctors for a specified specialization, date, and time. Patients can search for available doctors and choose from the list.

4. **Appointment Booking**: Patients can book appointments with their chosen doctor based on availability. The skill reserves the appointment slot in the doctor's Google Calendar and sends a confirmation email to the patient.

5. **Voice-Based Doctor Recommendations**: Implement a feature that allows Alexa to recommend doctors based on the patient's symptoms or medical conditions. Users can ask Alexa for suggestions, and the skill can provide a list of doctors specializing in relevant fields.

6. **Voice Authentication**: Integrate voice authentication technology to improve security during the registration and login process. This can enhance the skill's ability to verify the identity of patients securely.

7. **Email Notifications**: The skill uses Amazon SES to send verification emails to new patients and confirmation emails for scheduled appointments.

8. **Insurance Information Integration**: Enable the skill to retrieve and store insurance information for patients. This can help streamline billing and insurance processing.

## Tech Stack

The Hospital Appointment Scheduler skill is built using the following technologies:

- **Alexa Skills Kit (ASK)**: A collection of APIs and tools for building voice-driven experiences.
- **AWS Lambda**: A serverless compute service for running code in response to Alexa requests.
- **AWS DynamoDB**: A NoSQL database service for storing patient and doctor information.
- **Google Calendar API**: An API for managing Google Calendar events and availability.
- **Amazon Simple Email Service (SES)**: A service for sending emails to users.

## Work Flow

![image](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/96c227b5-3b8c-444a-9814-60e46f088457)


## Skill Features

### User Registration and Verification

- New patients can register by providing their full name, age, gender, DOB, father's name, and email.
- The skill sends a verification email to the provided email address for identity confirmation.
- Returning patients can log in using their patient ID or verify their identity using their father's name.

### Doctor Availability Checking

- Patients can search for available doctors based on a specified specialization, date, and time.
- The skill uses the Google Calendar API to check the availability of doctors for the specified time slot.

### Appointment Booking

- Patients can schedule appointments with their chosen doctor based on availability.
- The skill reserves the appointment slot in the doctor's Google Calendar.

### Voice-Based Doctor Recommendations

- Alexa can provide doctor recommendations based on the patient's symptoms or medical conditions.
- Users can ask Alexa for suggestions, and the skill will offer a list of doctors specializing in relevant fields.

### Voice Authentication

- The skill can use voice authentication technology for secure user registration and login.

### Email Notifications

- The skill sends verification emails to new patients for identity confirmation.
- Confirmation emails for scheduled appointments are sent to patients' registered email addresses.

## Lambda Function Code

The Lambda function for the Hospital Appointment Scheduler skill is responsible for handling user requests and interacting with the backend services. It is written in Python and integrated with the ASK SDK for Alexa interactions. The code is structured into several intent handlers to handle different user intents, such as registration, login, appointment booking, doctor recommendations, and more.

**Code Link:** https://drive.google.com/file/d/1bd1YhIb3PICCIkCkxA7kR7VNLLx1PAk4/view?usp=sharing

## Skill Invocation and User Flow

1. **Skill Launch**: Users can invoke the skill by saying "Alexa, open Hospital Appointment Scheduler."

2. **New Patient**: New patients can provide their information during the registration process. The skill will send a verification email to the provided email address.

3. **Verification**: New patients need to verify their email by following the instructions in the verification email.

4. **Returning Patient**: Returning patients can log in using their patient ID. If they forget their ID, they can verify their identity by providing their father's name.

5. **Doctor Availability Checking**: Patients can check the availability of doctors based on specialization, date, and time.

6. **Appointment Booking**: Patients can book appointments with available doctors.

7. **Voice-Based Doctor Recommendations**: Patients can ask Alexa for doctor recommendations based on their symptoms or medical conditions.

8. **Voice Authentication**: The skill uses voice authentication for user identity verification during registration and login.

9. **Email Notifications**: Verification emails are sent to new patients, and confirmation emails are sent for scheduled appointments.


## Working with New Patients

New patients can efficiently register and schedule appointments through the Hospital Appointment Scheduler skill. Below is a step-by-step guide on how new patients can utilize the skill:

1.	**Skill Invocation**: New patients can initiate the skill by saying "Alexa, open Hospital Appointment Scheduler."

2.	**Registration**: Alexa will guide the new patient through the registration process. The patient needs to provide the following information:

   
      • Full Name
  	
      • Age
  	
      • Gender
  	
      • Date of Birth (DOB)
  	
      • Father's Name
  	
      • Email Address


4.	**Email Verification**: After registration, the skill will send a verification email to the provided email address. The patient must check their email and follow the instructions to complete the verification process.

5.	**Account Creation**: Once the email is verified, the skill will create a unique patient ID for the new patient. The patient can use this ID for future logins.

6.	**Doctor Availability Checking**: New patients can inquire about doctor availability based on their preferred specialization, date, and time.

7.	**Appointment Booking**: After selecting a suitable doctor and appointment slot, the patient can proceed to book the appointment. Alexa will confirm the booking and send a confirmation email to the patient.


![mainimg1](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/e12fbd32-e859-4e52-9d99-f1a66c394efc)

![mainimg2](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/8df9fdf0-be12-40f6-abb0-4a937f68265e)


## Working with Returning Patients
Returning patients can conveniently access their accounts and manage appointments through the Hospital Appointment Scheduler skill. Here's a step-by-step guide on how returning patients can use the skill:

1.	**Skill Invocation**: Returning patients can launch the skill by saying "Alexa, open Hospital Appointment Scheduler."

2.	**Returning Patient Login**: Alexa will prompt the returning patient to provide their unique patient ID for authentication. The patient can say, "My patient ID is [patient ID]," to log in directly.

3.	**Appointment Management**: Once logged in, returning patients can manage their appointments with ease. They can schedule appointments, check available doctors by giving date, time and your required specialization.

4.	**Doctor Recommendations**: Returning patients can also ask for doctor recommendations based on their medical condition or symptoms. Alexa will provide a list of doctors specializing in relevant fields to help them make informed decisions.

5.	**Appointment Booking**: After selecting a suitable doctor and appointment slot, the patient can proceed to book the appointment. Alexa will confirm the booking and send a confirmation email to the patient.


![mainimg1](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/682f414d-a670-4249-85b0-ec1d6aed71ea)

![mainimg2](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/f3c56acd-461a-46c4-b9cd-383f2c6a1800)



## In case if you forgot your Patient ID
-->**Forgot Patient ID**: In case the patient forgets their patient ID, Alexa will offer an alternative way to verify their identity. The patient can say, "I forgot my patient ID," and Alexa will ask for their father's name for verification.


![img10](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/e1626c00-8bc2-4e25-961b-d3364c4b8aa2)


## Emails you get while working with the skill
We used a fake email to chech wheather it is working ....
## Verification Email
![mainimg1](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/c28befa8-abf8-447b-8ce9-7ef8b5f1a410)
## Conformation page
![mainimg3](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/d451583c-3de5-4029-9d18-e2d8af546194)
## Details Email
![mainimg2](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/b6191d1b-705f-4f57-8340-826c23461838)
## Appointment Scheduled Email
![img10](https://github.com/katakampranav/Hospital-Appointment-Scheduler-using-Alexa/assets/133202118/1bf5af2c-173b-4e37-bc23-c506c693d19a)

## Applications

1. **Voice-Based Doctor Recommendations**: Implement a feature that allows Alexa to recommend doctors based on the patient's symptoms or medical conditions. Users can ask Alexa for suggestions, and the skill can provide a list of doctors specializing in relevant fields.

2. **Appointment Reminders**: Enable the skill to send appointment reminders to patients a day or a few hours before their scheduled appointment. This can help reduce no-shows and improve overall patient attendance.

3. **Multilingual Support**: Extend the skill's capabilities to support multiple languages. Patients from diverse linguistic backgrounds can then interact with the skill in their preferred language.

4. **Voice Authentication**: Integrate voice authentication technology to improve security during the registration and login process. This can enhance the skill's ability to verify the identity of patients securely.

5. **Emergency Services**: Add emergency response capabilities, where users can request immediate medical assistance or information during critical situations.

## Author

The Hospital Appointment Scheduler using Alexa skill was developed by "Pranav Shankar".

## Feedback

For any feedback or queries, please reach out to the author at katakampranavshankar@gmail.com.
