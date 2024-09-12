# Use an official PHP runtime as a parent image
FROM php:7.4-apache

# Set the working directory inside the container
WORKDIR /var/www/html

# Copy the contents of the src directory into the working directory inside the container
COPY src/ /var/www/html/

# Expose port 80 to the outside world (you map to 92 on your local machine)
EXPOSE 80

# Enable Apache mod_rewrite for clean URLs (optional, if needed)
RUN a2enmod rewrite

# Start Apache in the foreground
CMD ["apache2-foreground"]

