from flask import Flask, request, jsonify
import linkedin_scraper as scraper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    job_title = data.get('jobTitle')
    company_name = data.get('companyName')
    max_results = 10  # Set the maximum number of profiles to process
    profile_ids = scraper.linkedin_resume_search(job_title, company_name, max_results)

    results = []
    processed_count = 0
    for urn_id in profile_ids:
        if processed_count >= max_results:
            break  # Stop if maximum profiles processed

        profile = scraper.get_linkedin_profile(urn_id)
        if profile and profile.get("summary") and profile.get("potential_link"):
            resume_link = scraper.extract_resume_link_with_langchain(profile["summary"])
            if resume_link:
                results.append({
                    "name": f"{profile['first_name']} {profile['last_name']}",
                    "resume_link": resume_link
                })
                print("found resume link")

        processed_count += 1  # Increment the processed profile count

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
