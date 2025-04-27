from datetime import date
from flask_bcrypt import Bcrypt
from models import User, Educator, Subject, Chapter, Quiz, Question, Admin

bcrypt = Bcrypt()

users = [
    User(username="gauri03", password=bcrypt.generate_password_hash("gauri123").decode("utf-8"), dob=date(2003, 1, 1), qualification="B.E. Computer Science"),
    User(username="anaya04", password=bcrypt.generate_password_hash("anaya123").decode("utf-8"), dob=date(2004, 2, 2), qualification="B.Tech. Information Science"),
    User(username="megha05", password=bcrypt.generate_password_hash("megha123").decode("utf-8"), dob=date(2005, 3, 3), qualification="B.Sc. IT"),
]

educators = [
    Educator(username="ravi_educ", password=bcrypt.generate_password_hash("ravi123").decode("utf-8"), qualification="PhD in CS", fullname="Dr. Ravi Sharma"),
    Educator(username="neha_educ", password=bcrypt.generate_password_hash("neha123").decode("utf-8"), qualification="PhD in Data Science", fullname="Dr. Neha Kapoor"),
    Educator(username="sita_educ", password=bcrypt.generate_password_hash("sita123").decode("utf-8"), qualification="M.Tech in Software Engineering", fullname="Sita Verma"),
]

subjects = [
    Subject(name="Modern Application Development", description="Focus on scalable, cloud-native applications.", educator_id=1),
    Subject(name="Business Data Management", description="Managing data across business platforms.", educator_id=2),
    Subject(name="Data Science Fundamentals", description="Introduction to data science concepts.", educator_id=3),
    Subject(name="Web Development Basics", description="Foundational concepts of web development.", educator_id=1),
    Subject(name="Database Management Systems", description="Understanding DBMS concepts and applications.", educator_id=2),
    Subject(name="Cloud Computing", description="Basics of cloud computing and services.", educator_id=3),
]

chapters = [
    Chapter(name="Intro to Modern App Dev", description="Introduction to MAD concepts.", content="""Cloud-native applications are scalable and designed to be deployed on cloud platforms. These applications leverage cloud infrastructure to manage computing resources and store data. One of the key principles of cloud-native development is the use of microservices, which allows each component of an application to be independently developed, deployed, and scaled.

In the early days of computing, applications were tightly coupled to the hardware and operating system. However, with the advent of cloud computing, applications can now be built and hosted on distributed systems, making them more resilient and easier to scale. Cloud-native applications are usually developed using agile methodologies, which prioritize iterative development, customer feedback, and cross-functional collaboration.

This chapter explores the fundamental concepts of cloud-native development, including microservices, containerization, continuous delivery, and cloud infrastructure. We will discuss the benefits and challenges of cloud-native development and explore how modern tools like Kubernetes and Docker enable cloud-native applications to thrive.""", subject_id=1),
    Chapter(name="Data Models & Design", description="Core concepts of data modeling.", content="""
Scalability is the ability of a system to handle increasing amounts of work or its potential to accommodate growth. In cloud-native application development, scalability is achieved by leveraging cloud infrastructure, which can be easily scaled up or down depending on the demand. This is done using services like Amazon EC2, Google Cloud Compute, and Azure Virtual Machines.

There are two main types of scalability:
1. Vertical Scalability (Scaling Up): This involves adding more resources (CPU, RAM, storage) to a single machine to handle increased load. It is typically easier to implement but has its limits.
2. Horizontal Scalability (Scaling Out): This involves adding more machines or instances to handle increased load. Cloud-native applications are designed to take advantage of horizontal scalability, enabling them to handle traffic spikes and growth in user base.

In addition to scalability, cloud-native applications also focus on resilience. This means that if one component fails, the entire system should not go down. This chapter covers strategies for building scalable and resilient cloud-native applications, including load balancing, auto-scaling, and disaster recovery techniques.
    """, subject_id=2),
    Chapter(name="Web Dev Basics", description="Foundational concepts of web development.", content="""
Business data management refers to the practices, policies, and tools used by organizations to ensure that their data is accurate, consistent, and accessible. Effective data management is critical to business decision-making, as it helps ensure that reliable data is available when needed.

The first principle of data management is data governance, which involves defining policies and procedures for handling data. This includes ensuring that data is classified correctly, and there are clear rules for its usage, storage, and sharing. Data governance also involves ensuring compliance with relevant regulations such as GDPR and HIPAA.

The second principle is data quality, which focuses on ensuring that the data is accurate, complete, and timely. Poor data quality can lead to incorrect decision-making, missed opportunities, and inefficiencies. This chapter discusses best practices for ensuring data quality, such as data validation, cleansing, and enrichment.

Finally, business data management also involves data integration, which is the process of combining data from multiple sources to provide a unified view. This is essential for organizations that rely on multiple systems and databases to store their data. We will explore different techniques for data integration, including ETL (Extract, Transform, Load) processes and real-time data streaming.
    """, subject_id=4),
    Chapter(name="DBMS Concepts", description="Understanding DBMS concepts and applications.", content="ACID properties, transactions, indexing.", subject_id=5),
    Chapter(name="Cloud Services", description="Basics of cloud computing and services.", content="IaaS, PaaS, SaaS models.", subject_id=6),
    Chapter(name="Data Science Overview", description="Introduction to data science concepts.", content="Data collection, cleaning, and analysis.", subject_id=3),
    Chapter(name="Frontend Technologies", description="Overview of frontend technologies.", content="HTML, CSS, JavaScript frameworks.", subject_id=1),
    Chapter(name="Backend Technologies", description="Overview of backend technologies.", content="Node.js, Express, databases.", subject_id=1),
    Chapter(name="Data Warehousing", description="Understanding data warehousing concepts.", content="ETL processes, OLAP vs OLTP.", subject_id=2),
    Chapter(name="Data Visualization", description="Basics of data visualization.", content="Tools and techniques for visualizing data.", subject_id=3),    
    Chapter(name="Cloud Security", description="Understanding cloud security principles.", content="Data encryption, access control.", subject_id=6),
    Chapter(name="Data Mining", description="Basics of data mining techniques.", content="Classification, clustering, regression.", subject_id=3),
]

quizzes = [
    Quiz(name="MAD Quiz 1", description="Covers basics of web development.", subject_id=1),
    Quiz(name="MAD Quiz 2", description="Focus on frontend & cloud-native architecture.", subject_id=1),
    Quiz(name="BDM Quiz 1", description="Covers ER diagrams and DBMS concepts.", subject_id=2),
    Quiz(name="BDM Quiz 2", description="Advanced SQL and data lifecycle.", subject_id=2),
    Quiz(name="DS Quiz 1", description="Basics of data science and analytics.", subject_id=3),
    Quiz(name="DS Quiz 2", description="Intermediate data science concepts.", subject_id=3),    
]

questions = [
    # MAD Quiz 1
    Question(quiz_id=1, statement="What does MAD stand for in software engineering?", option_a="Make And Deploy", option_b="Modern App Development", option_c="Modular API Design", option_d="Mainframe App Development", correct_answer="Modern App Development"),
    Question(quiz_id=1, statement="Which of these is a frontend technology?", option_a="Django", option_b="Flask", option_c="React", option_d="MySQL", correct_answer="React"),
    Question(quiz_id=1, statement="Which protocol does HTTP use for secure communication?", option_a="FTP", option_b="TCP", option_c="HTTPS", option_d="SSL", correct_answer="HTTPS"),
    Question(quiz_id=1, statement="Which of the following is a NoSQL database?", option_a="PostgreSQL", option_b="MySQL", option_c="MongoDB", option_d="SQLite", correct_answer="MongoDB"),
    Question(quiz_id=1, statement="What does REST stand for?", option_a="Representational State Transfer", option_b="Remote Secure Transfer", option_c="Recursive Script Template", option_d="Rapid Execution System Transfer", correct_answer="Representational State Transfer"),
    Question(quiz_id=1, statement="Which HTML tag is used to create a hyperlink?", option_a="<link>", option_b="<a>", option_c="<href>", option_d="<url>", correct_answer="<a>"),
    Question(quiz_id=1, statement="Which language is used for styling web pages?", option_a="HTML", option_b="Python", option_c="CSS", option_d="Java", correct_answer="CSS"),
    Question(quiz_id=1, statement="What is the default port for HTTP?", option_a="80", option_b="443", option_c="21", option_d="3306", correct_answer="80"),
    Question(quiz_id=1, statement="Which of these is a frontend JS framework?", option_a="Vue.js", option_b="Django", option_c="Laravel", option_d="Flask", correct_answer="Vue.js"),
    Question(quiz_id=1, statement="What is the purpose of a CDN?", option_a="Content Delivery Network", option_b="Cloud Data Node", option_c="Central Data Network", option_d="Client Developer Node", correct_answer="Content Delivery Network"),

    # MAD Quiz 2
    Question(quiz_id=2, statement="What does SPA stand for in web development?", option_a="Single Page Application", option_b="Software Page Architecture", option_c="Static Page App", option_d="Script Powered App", correct_answer="Single Page Application"),
    Question(quiz_id=2, statement="Which cloud provider offers S3 buckets?", option_a="Google Cloud", option_b="AWS", option_c="Azure", option_d="IBM Cloud", correct_answer="AWS"),
    Question(quiz_id=2, statement="Which HTTP verb is used to create data?", option_a="GET", option_b="POST", option_c="DELETE", option_d="FETCH", correct_answer="POST"),
    Question(quiz_id=2, statement="What is containerization in DevOps?", option_a="Storing files in the cloud", option_b="Running software in isolated environments", option_c="Packaging databases", option_d="Clustering VMs", correct_answer="Running software in isolated environments"),
    Question(quiz_id=2, statement="What tool is used to manage containers?", option_a="GitHub", option_b="Kubernetes", option_c="Ansible", option_d="Nginx", correct_answer="Kubernetes"),
    Question(quiz_id=2, statement="Which HTTP status code indicates success?", option_a="400", option_b="401", option_c="200", option_d="500", correct_answer="200"),
    Question(quiz_id=2, statement="What’s a common build tool for React apps?", option_a="Webpack", option_b="Maven", option_c="Gulp", option_d="Gradle", correct_answer="Webpack"),
    Question(quiz_id=2, statement="Which of these is a PaaS provider?", option_a="Heroku", option_b="MySQL", option_c="Git", option_d="Jenkins", correct_answer="Heroku"),
    Question(quiz_id=2, statement="Which keyword is used to declare a constant in JavaScript?", option_a="var", option_b="let", option_c="const", option_d="define", correct_answer="const"),
    Question(quiz_id=2, statement="What does CORS deal with?", option_a="Database replication", option_b="Cross-origin resource sharing", option_c="Cache optimization", option_d="REST API testing", correct_answer="Cross-origin resource sharing"),

    # BDM Quiz 1
    Question(quiz_id=3, statement="What does ER in ER diagram stand for?", option_a="Entity-Relationship", option_b="Event-Response", option_c="Entity-Redundancy", option_d="Event-Relay", correct_answer="Entity-Relationship"),
    Question(quiz_id=3, statement="Which of the following is a primary key?", option_a="A unique identifier", option_b="A repeated value", option_c="A foreign key", option_d="An attribute with NULLs", correct_answer="A unique identifier"),
    Question(quiz_id=3, statement="Which language is used for querying databases?", option_a="HTML", option_b="SQL", option_c="CSS", option_d="JavaScript", correct_answer="SQL"),
    Question(quiz_id=3, statement="Normalization helps in:", option_a="Data duplication", option_b="Query performance", option_c="Reducing redundancy", option_d="Increasing table size", correct_answer="Reducing redundancy"),
    Question(quiz_id=3, statement="Which of the following is not a DBMS?", option_a="MySQL", option_b="MongoDB", option_c="Oracle", option_d="Docker", correct_answer="Docker"),
    Question(quiz_id=3, statement="Which SQL keyword is used to get all records?", option_a="SELECT", option_b="SHOW", option_c="RETRIEVE", option_d="GET", correct_answer="SELECT"),
    Question(quiz_id=3, statement="Which key connects two tables?", option_a="Primary Key", option_b="Composite Key", option_c="Foreign Key", option_d="Unique Key", correct_answer="Foreign Key"),
    Question(quiz_id=3, statement="Data integrity ensures:", option_a="Storage efficiency", option_b="Security", option_c="Accuracy and consistency", option_d="Replication", correct_answer="Accuracy and consistency"),
    Question(quiz_id=3, statement="Which of the following is a relational database?", option_a="Firebase", option_b="MongoDB", option_c="PostgreSQL", option_d="Redis", correct_answer="PostgreSQL"),
    Question(quiz_id=3, statement="Which operation combines rows from two tables?", option_a="Join", option_b="Select", option_c="Insert", option_d="Merge", correct_answer="Join"),

    # BDM Quiz 2
    Question(quiz_id=4, statement="Which SQL clause is used to filter records?", option_a="ORDER BY", option_b="WHERE", option_c="GROUP BY", option_d="HAVING", correct_answer="WHERE"),
    Question(quiz_id=4, statement="Which command is used to delete a table?", option_a="REMOVE TABLE", option_b="DELETE", option_c="DROP", option_d="ERASE", correct_answer="DROP"),
    Question(quiz_id=4, statement="In which normal form do transitive dependencies get eliminated?", option_a="1NF", option_b="2NF", option_c="3NF", option_d="BCNF", correct_answer="3NF"),
    Question(quiz_id=4, statement="Which SQL function returns the number of rows?", option_a="SUM()", option_b="COUNT()", option_c="ROWNUM()", option_d="LENGTH()", correct_answer="COUNT()"),
    Question(quiz_id=4, statement="A data warehouse is used for:", option_a="Transactional processing", option_b="Operational queries", option_c="Analytical processing", option_d="Data cleanup", correct_answer="Analytical processing"),
    Question(quiz_id=4, statement="Which language is used for data analysis in BDM?", option_a="R", option_b="C++", option_c="Java", option_d="Ruby", correct_answer="R"),
    Question(quiz_id=4, statement="ETL stands for:", option_a="Extract Transform Load", option_b="Evaluate Test Load", option_c="Enter Transform Launch", option_d="Execute Trace Load", correct_answer="Extract Transform Load"),
    Question(quiz_id=4, statement="Which command updates data in SQL?", option_a="MODIFY", option_b="ALTER", option_c="UPDATE", option_d="SET", correct_answer="UPDATE"),
    Question(quiz_id=4, statement="What does OLAP stand for?", option_a="Online Access Protocol", option_b="Object Logic App", option_c="Online Analytical Processing", option_d="Open Learning Access Program", correct_answer="Online Analytical Processing"),
    Question(quiz_id=4, statement="Which of these is a columnar DB?", option_a="MySQL", option_b="Cassandra", option_c="Redis", option_d="ClickHouse", correct_answer="ClickHouse"),

    # DS Quiz 1
    Question(quiz_id=5, statement="What does DS stand for?", option_a="Data Science", option_b="Data Structure", option_c="Data Storage", option_d="Data Security", correct_answer="Data Science"),
    Question(quiz_id=5, statement="Which of the following is a data visualization tool?", option_a="Tableau", option_b="MySQL", option_c="Python", option_d="Java", correct_answer="Tableau"),
    Question(quiz_id=5, statement="Which library is commonly used for data manipulation in Python?", option_a="NumPy", option_b="Pandas", option_c="Matplotlib", option_d="Seaborn", correct_answer="Pandas"),
    Question(quiz_id=5, statement="What is the purpose of data cleaning?", option_a="Data storage", option_b="Data analysis", option_c="Data visualization", option_d="Data preparation", correct_answer="Data preparation"),
    Question(quiz_id=5, statement="Which algorithm is used for classification?", option_a="K-Means", option_b="Linear Regression", option_c="Decision Tree", option_d="KNN", correct_answer="Decision Tree"),
    Question(quiz_id=5, statement="What does the term 'Big Data' refer to?", option_a="Small datasets", option_b="Large and complex datasets", option_c="Structured data only", option_d="Data in the cloud", correct_answer="Large and complex datasets"),
    Question(quiz_id=5, statement="Which of the following is a supervised learning algorithm?", option_a="K-Means", option_b="Linear Regression", option_c="PCA", option_d="Hierarchical Clustering", correct_answer="Linear Regression"),
    Question(quiz_id=5, statement="What is the purpose of data normalization?", option_a="Data encryption", option_b="Data compression", option_c="Scaling data to a specific range", option_d="Data visualization", correct_answer="Scaling data to a specific range"),
    Question(quiz_id=5, statement="Which of the following is a clustering algorithm?", option_a="K-Means", option_b="Linear Regression", option_c="Logistic Regression", option_d="Decision Tree", correct_answer="K-Means"),
    Question(quiz_id=5, statement="What is the purpose of a confusion matrix?", option_a="Data storage", option_b="Model evaluation", option_c="Data cleaning", option_d="Data visualization", correct_answer="Model evaluation"),

]
