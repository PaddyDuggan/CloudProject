# Use a Gradle image with OpenJDK 18 to build the application
FROM gradle:7.5.1-jdk18 AS build
WORKDIR /app
COPY --chown=gradle:gradle . /app

# Build the application
RUN gradle build -x test

# Use a smaller base image with JRE 18 to run the application
FROM openjdk:18-slim  
WORKDIR /app
COPY --from=build /app/build/libs/*.jar /app/ipchecker.jar

# Expose the port
EXPOSE 8080

# Command to run the application
CMD ["java", "-jar", "ipchecker.jar"]



