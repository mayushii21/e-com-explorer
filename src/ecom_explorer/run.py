from ecom_explorer.layout import app

# Create server for gunicorn
server = app.server


def main():
    app.run(debug=False)


if __name__ == "__main__":
    main()
