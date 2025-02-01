from flask_app import app

def main():
    # Run the command line application
    app.run(host="0.0.0.0",port=5000)
if __name__ == "__main__":
    # Run the Flask app in a separate process
    print("Flask server is running on http://127.0.0.1:5000")
    main()
    print("Flask server stopped.")
    