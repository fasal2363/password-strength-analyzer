from flask import Flask, render_template, request
import hashlib
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        password = request.form["password"]

        length = len(password)

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)

        special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/"
        has_special = any(c in special_chars for c in password)

        score = 0

        if length >= 8:
            score += 1

        if has_upper:
            score += 1

        if has_lower:
            score += 1

        if has_digit:
            score += 1

        if has_special:
            score += 1

        if score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Moderate"
        else:
            strength = "Strong"

        charset = 0

        if has_lower:
            charset += 26

        if has_upper:
            charset += 26

        if has_digit:
            charset += 10

        if has_special:
            charset += 32

        entropy = 0

        if charset > 0:
            entropy = round(length * math.log2(charset), 2)

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        result = {
            "strength": strength,
            "score": score,
            "entropy": entropy,
            "hash": hashed_password
        }

    return render_template(
        "index.html",
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)