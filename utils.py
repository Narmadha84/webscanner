# utils.py

def get_form_details(form):
    details = {
        "action": form.get("action"),
        "method": form.get("method", "get").lower(),
        "inputs": []
    }
    for input_tag in form.find_all("input"):
        name = input_tag.get("name")
        input_type = input_tag.get("type", "text")
        details["inputs"].append({"name": name, "type": input_type})
    return details
