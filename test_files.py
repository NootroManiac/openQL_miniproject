import atheris
import sys
import detectors.email_detector as email_detector
import string 


'''
def email_Mutator(data, max_size, seed):
    email_data = {
            "subject": string[:12],  
            "body": string,         
            "sender": "test@example.com"  
        }
    
    try:
        json_str = data.decode("utf-8", errors="ignore")
        email_data["subject"] = json_str[:12]
        email_data["body"] = json_str
        email_data["sender"] = "fuzzer@example.com"
    except :
        email_data = {
            "subject": "Hello world!",
            "body": "This is the body of the email.",
            "sender": "fuzzer@example.com"
        }
    return email_data
'''
def TestPointOne(data):
    fdp = atheris.FuzzedDataProvider(data)
    email_data = {
            "subject": fdp.ConsumeString(12),  
            "body": fdp.ConsumeString(1000),         
            "sender": "test@example.com"  
    }
    

    try:
        email_detector.EmailDetector.analyze(email_data) 
    except:
        pass

atheris.Setup(sys.argv, TestPointOne)
atheris.Fuzz()