# gradle

JVM builds with Gradle (and the Maven equivalents); tasks, deps, the wrapper.

## Gradle (prefer the wrapper)

```bash
./gradlew tasks                        # list available tasks
./gradlew build                        # compile + test + assemble
./gradlew test --tests '*UserServiceTest'
./gradlew bootRun                      # run a Spring Boot app
./gradlew dependencies                 # dependency tree
```

## Maven equivalents

```bash
mvn clean package                      # build + test + jar
mvn test -Dtest=UserServiceTest
mvn dependency:tree                    # dependency tree
mvn -o package                         # offline build (use cache)
```

## Notes

- Commit the `gradlew` / `mvnw` wrapper so builds are reproducible everywhere
- `--offline` (gradle) / `-o` (maven) for air-gapped or cache-only builds
- `./gradlew build --scan` produces a shareable build report
