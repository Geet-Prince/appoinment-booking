import streamlit as st
from datetime import datetime, timedelta
from data import hospitals, doctors, generate_all_slots  # Ensure correct import path

# Generate slots if not imported directly
slots = generate_all_slots()

def show_hospitals():
    st.title("Hospital Appointment Booking")
    hospital_names = [hospital["name"] for hospital in hospitals]
    selected_hospital_name = st.selectbox("Select a Hospital", hospital_names)
    selected_hospital_id = next(hospital["id"] for hospital in hospitals if hospital["name"] == selected_hospital_name)
    
    st.session_state.selected_hospital_name = selected_hospital_name
    return selected_hospital_id

def show_doctors(hospital_id):
    doctor_list = doctors.get(hospital_id, [])
    doctor_names = [doctor["name"] for doctor in doctor_list]
    selected_doctor_name = st.selectbox("Select a Doctor", doctor_names)
    selected_doctor_id = next(doctor["id"] for doctor in doctor_list if doctor["name"] == selected_doctor_name)
    
    st.session_state.selected_doctor_name = selected_doctor_name
    return selected_doctor_id

def show_slots(hospital_id, doctor_id):
    today = datetime.today().date()  # Use .date() for comparison
    max_date = today + timedelta(weeks=1)
    
    date = st.date_input(
        "Select a Date", 
        min_value=today, 
        max_value=max_date,
        value=today
    )
    
    datetime_str = date.strftime("%Y-%m-%d")
    
    available_slots = slots.get(doctor_id, {}).get(datetime_str, [])
    slots_for_date = [slot for slot in available_slots if slot.startswith(datetime_str)]
    
    if slots_for_date:
        selected_slot = st.radio("Select an Appointment Slot", slots_for_date)
    else:
        st.text("No slots available")
        selected_slot = None

    return selected_slot

def enter_patient_details():
    st.title("Enter Patient Details")
    
    # Use a form context to handle form submission
    with st.form(key='patient_form'):
        # Collect user input
        name = st.text_input("Name")
        address = st.text_input("Address")
        mobile_number = st.text_input("Mobile Number", max_chars=10)  # Limit to 10 digits
        
        # Initialize an empty list for errors
        errors = []
        
        # Validate inputs
        if not name:
            errors.append("Name is required.")
        if not address:
            errors.append("Address is required.")
        if not mobile_number:
            errors.append("Mobile Number is required.")
        elif not mobile_number.isdigit():
            errors.append("Mobile Number must be digits only.")
        elif len(mobile_number) != 10:
            errors.append("Mobile Number must be exactly 10 digits long.")
        
        # Display errors if there are any
        if errors:
            st.error(" ".join(errors))
            st.form_submit_button("Submit")  
            return  # Exit the function without processing further
        
        # If no errors, add a submit button to process the form
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            # Save patient details in session state
            st.session_state.patient_details = {
                "name": name,
                "address": address,
                "mobile_number": mobile_number
            }
            # Proceed to the confirmation step
            st.session_state.step = 'confirmation'

def generate_download(patient_details, hospital_name, doctor_name, slot):
    # Prepare details as a text file content
    details = f"""Appointment Details:
    Name: {patient_details['name']}
    Address: {patient_details['address']}
    Mobile Number: {patient_details['mobile_number']}
    Hospital: {hospital_name}
    Doctor: {doctor_name}
    Slot: {slot}
    """
    
    return details

def confirmation_page():
    st.title("Confirmation")
    
    if 'patient_details' in st.session_state:
        details = st.session_state.patient_details
        
        if not details.get("name") or not details.get("address") or not details.get("mobile_number"):
            st.error("Please fill in all details before confirming.")
            st.session_state.step = 'details'
            return
        
        st.write(f"Name: {details['name']}")
        st.write(f"Address: {details['address']}")
        st.write(f"Mobile Number: {details['mobile_number']}")
        
        selected_hospital_name = st.session_state.selected_hospital_name
        selected_doctor_name = st.session_state.selected_doctor_name
        selected_slot = st.session_state.selected_slot
        
        st.write(f"Hospital: {selected_hospital_name}")
        st.write(f"Doctor: {selected_doctor_name}")
        st.write(f"Appointment Slot: {selected_slot}")
        
        if st.button("Confirm Booking"):
            st.success("Appointment booked successfully!")
            
            # Generate the downloadable file content
            download_content = generate_download(details, selected_hospital_name, selected_doctor_name, selected_slot)
            
            # Provide the download button, pass the download_content as string
            st.download_button(
                label="Download Appointment Details",
                data=download_content,  # Pass the string content here
                file_name=f"{details['name']}_appointment_details.txt",
                mime="text/plain"
            )
            
            # Clear session state after booking
            del st.session_state.step
            del st.session_state.patient_details
    else:
        st.error("No patient details found")

def main():
    if 'step' not in st.session_state:
        st.session_state.step = 'hospital_selection'

    if st.session_state.step == 'hospital_selection':
        selected_hospital_id = show_hospitals()
        if 'selected_hospital_id' not in st.session_state:
            st.session_state.selected_hospital_id = selected_hospital_id
        else:
            selected_hospital_id = st.session_state.selected_hospital_id

        selected_doctor_id = show_doctors(selected_hospital_id)
        if 'selected_doctor_id' not in st.session_state:
            st.session_state.selected_doctor_id = selected_doctor_id
        else:
            selected_doctor_id = st.session_state.selected_doctor_id

        selected_slot = show_slots(selected_hospital_id, selected_doctor_id)
        
        if st.button("Book Appointment"):
            if selected_slot:
                st.session_state.selected_slot = selected_slot
                st.session_state.step = 'details'
            else:
                st.error("Please select a slot")

    elif st.session_state.step == 'details':
        enter_patient_details()
    
    elif st.session_state.step == 'confirmation':
        confirmation_page()

if __name__ == "__main__":
    main()
