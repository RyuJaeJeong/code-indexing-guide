## 인터넷이 원활한 경우
 
scip-java 관련 압축 파일 다운로드 후, image 를 load 해 준다
```cmd
podman load -i scip-java.tar
```

프로젝트 경로로 이동 후, scip 파일 저장 후, 아래 명령어를 실행한다 
```cmd
podman run -v "%cd%:/sources" --env JVM_VERSION=8 sourcegraph/scip-java:latest /bin/sh -c "scip-java index && ./scip print --json index.scip > index.json"
```

프로젝트 빌드가 정상적으로 실행 가능한 경우, 


## 인터넷이 원활하지 않은 경우
semantic-db 플러그인 등록
```cmd
mvn install:install-file -Dfile=semanticdb-javac-0.11.2.jar -DgroupId=com.sourcegraph -DartifactId=semanticdb-javac -Dversion=0.11.2 -Dpackaging=jar
```
pom.xml 수정 
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <configuration>
                <annotationProcessorPaths>
                    <path>
                        <groupId>org.projectlombok</groupId>
                        <artifactId>lombok</artifactId>
                    </path>
                    <path>
                        <groupId>com.sourcegraph</groupId>
                        <artifactId>semanticdb-javac</artifactId>
                        <version>0.11.2</version>
                    </path>
                </annotationProcessorPaths>
                <compilerArgs>
                    <arg>-Xplugin:semanticdb -sourceroot:${project.basedir} -targetroot:${project.build.directory}/classes</arg>
                </compilerArgs>
            </configuration>
        </plugin>
    </plugins>
</build>
```

SemanticDB 로컬 빌드 
```cmd
mvn clean compile
```
scip 생성, json 파일 생성
```cmd
podman run -v "%cd%:/sources" sourcegraph/scip-java:latest /bin/sh -c "scip-java index-semanticdb --output /sources/index.scip /sources/target/classes/META-INF/semanticdb && ./scip print --json index.scip > index.json"
```