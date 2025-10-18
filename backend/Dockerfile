FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app
COPY . /app
RUN ./gradlew -q clean bootJar --no-daemon || true

FROM eclipse-temurin:21-jdk-alpine
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
