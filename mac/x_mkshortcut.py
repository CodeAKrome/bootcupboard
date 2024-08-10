import plistlib
import uuid
import base64
import os

def create_mac_shortcut(name, actions):
    shortcut_data = {
        "WFWorkflowActions": actions,
        "WFWorkflowIcon": {
            "WFWorkflowIconStartColor": 4282601983,
            "WFWorkflowIconGlyphNumber": 59511
        },
        "WFWorkflowImportQuestions": [],
        "WFWorkflowTypes": ["NCWidget", "WatchKit", "Automation"],
        "WFWorkflowInputContentItemClasses": [
            "WFAppStoreAppContentItem",
            "WFArticleContentItem",
            "WFContactContentItem",
            "WFDateContentItem",
            "WFEmailAddressContentItem",
            "WFGenericFileContentItem",
            "WFImageContentItem",
            "WFiTunesProductContentItem",
            "WFLocationContentItem",
            "WFDCMapsLinkContentItem",
            "WFAVAssetContentItem",
            "WFPDFContentItem",
            "WFPhoneNumberContentItem",
            "WFRichTextContentItem",
            "WFSafariWebPageContentItem",
            "WFStringContentItem",
            "WFURLContentItem"
        ],
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowOutputContentItemClasses": ["WFStringContentItem"],
        "WFWorkflowActions": actions,
        "WFWorkflowName": name
    }
    
    # Generate a unique identifier for the shortcut
    shortcut_data['WFWorkflowActionIdentifier'] = str(uuid.uuid4()).upper()
    
    # Convert the dictionary to a plist
    plist_data = plistlib.dumps(shortcut_data)
    
    # Encode the plist data
    encoded_data = base64.b64encode(plist_data).decode('utf-8')
    
    # Create the .shortcut file
    filename = f"{name.replace(' ', '_')}.shortcut"
    with open(filename, 'w') as f:
        f.write(encoded_data)
    
    print(f"Shortcut '{name}' created as '{filename}'")

# Example usage
actions = [
    {
        "WFWorkflowActionIdentifier": "is.workflow.actions.showresult",
        "WFWorkflowActionParameters": {
            "Text": {"Value": {"String": "Hello, World!", "attachmentsByRange": {}}}
        }
    }
]

create_mac_shortcut("Hello World Shortcut", actions)
