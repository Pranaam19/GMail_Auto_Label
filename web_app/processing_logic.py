# web_app/processing_logic.py
import os
import json
from auto_label import gmail_api as original_gmail_api # For fetching/labeling
from auto_label import ai_util
from . import gmail_auth # For web authentication

USER_INFO_PATH = os.path.join(os.path.dirname(__file__), 'user_info.json')

def load_user_config():
    if not os.path.exists(USER_INFO_PATH):
        return None, None, None, "Error: user_info.json not found in web_app directory."
    with open(USER_INFO_PATH, 'r') as f:
        data = json.load(f)
    user_info_text = data.get('user_info', '')
    label_mapping = data.get('label_mapping', {})
    max_results = data.get('max_results', 10) # Default to 10 for web to keep it quick
    return user_info_text, label_mapping, max_results, None

def process_user_emails():
    results_log = []
    service = gmail_auth.get_gmail_service()
    if not service:
        return [{"id": "AUTH_ERROR", "subject": "Authentication", "label": "N/A", "reason": "Authentication failed. Please login or re-login.", "status": "ERROR"}]

    palm_api_key = os.getenv("PALM_API_KEY")
    if not palm_api_key:
        return [{"id": "CONFIG_ERROR", "subject": "Configuration", "label": "N/A", "reason": "PALM_API_KEY environment variable not set.", "status": "ERROR"}]

    user_info_text, label_mapping, max_results, error = load_user_config()
    if error:
        return [{"id": "CONFIG_ERROR", "subject": "Configuration", "label": "N/A", "reason": error, "status": "ERROR"}]

    try:
        messages = original_gmail_api.fetch_emails(service, max_results=max_results)
        if not messages:
            return [{"id": "INFO", "subject": "Email Fetch", "label": "N/A", "reason": "No new emails found to process.", "status": "INFO"}]

        # Get existing labels to avoid recreating them unnecessarily often
        # However, create_label has a check, so this is more an optimization
        # current_labels = original_gmail_api.list_labels(service)

        for message_id in messages:
            log_entry = {"id": message_id, "subject": "N/A", "label": "N/A", "reason": "N/A", "status": "PENDING"}
            try:
                email_content = original_gmail_api.fetch_email_content(service, message_id)
                log_entry["subject"] = email_content.get('subject', 'No Subject')

                # Ensure mail_body is not None
                mail_body = email_content.get('body')
                if mail_body is None:
                    log_entry["status"] = "FAILED"
                    log_entry["reason"] = "Email body is empty or could not be fetched."
                    results_log.append(log_entry)
                    continue

                ai_label, ai_reason = ai_util.mail_processor(
                    user_info=user_info_text,
                    label_mapping=label_mapping,
                    mail_body=mail_body,
                    llm_online=True,
                    api_key=palm_api_key
                )
                log_entry["label"] = ai_label
                log_entry["reason"] = ai_reason

                try:
                    original_gmail_api.add_label(service, message_id, ai_label)
                    log_entry["status"] = "SUCCESS"
                except KeyError: # Label might not exist
                    original_gmail_api.create_label(service, ai_label)
                    original_gmail_api.add_label(service, message_id, ai_label)
                    log_entry["status"] = "SUCCESS (Label Created)"

            except Exception as e:
                log_entry["status"] = "FAILED"
                log_entry["reason"] = str(e)
            results_log.append(log_entry)
    except Exception as e:
        return [{"id": "PROCESSING_ERROR", "subject": "General Processing", "label": "N/A", "reason": f"An error occurred during email processing: {str(e)}", "status": "ERROR"}]

    return results_log
