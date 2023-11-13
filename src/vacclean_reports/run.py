from vacclean_reports.layout import app

# Create server for gunicorn
server = app.server


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
