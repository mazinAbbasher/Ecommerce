# E-Commerce Application

Welcome to the E-Commerce Application! This server-side application is built with Django and provides a platform for managing and selling products online.

## Installation

To install and run the application using Docker and Docker Compose, follow these steps:

1. Clone the repository
2. Navigate to the project directory
3. Create a `.env` file in the project root directory and add the following environment variables:

   ````
   DATABASE_NAME=YOUR_DESIRED_DB_NAME
   DATABASE_USER=YOUR_DESIRED_DB_USER_NAME
   DATABASE_PASSWORD=YOUR_DESIRED_DB_PASSWORD
   DATABASE_ROOT_PASSWORD=YOUR_DESIRED_DB_ROOT_PASSWORD
   ALLOWED_HOSTS=['example.com', 'your_server_ip']
   '''Replace `example.com` with your actual domain name and `'your_server_ip'` with the IP address of your production server'''
   ENV="production"
   '''if you set ENV="development" then debug will be true, otherwise it  will be false'''
   SECRET_KEY="django-insecure-3ox5mvao2%k8$(=x2cz6v)i8bsta#)ftnnso6n_$08ly#4lpxo"
   ```

   Adjust the values according to your requirements.

4. Build and start the Docker containers using Docker Compose:

   ````
   docker-compose build
   docker-compose up -d
   ```

5. The application will be accessible at `http://your_server_ip:8001`. Replace `your_server_ip` with the IP address or hostname of your server.

## Development

If you would like to contribute to the project, follow these steps to set up a development environment:

1. Fork the repository on GitHub and clone it to your local machine.
2. Follow the installation instructions mentioned earlier.
3. Create a new branch for your feature or bug fix: `git checkout -b my-feature`
4. Make your changes and ensure that the tests pass.
5. Submit a pull request with your changes.

## Troubleshooting

If you encounter any issues or have questions about the application, please check the [issue tracker]for existing problems or open a new issue. For general support, you can contact me at mazinabbayo@gmail.com.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- This application uses the awesome [Django](https://www.djangoproject.com/) framework.

---
