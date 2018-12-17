# Information-Extraction-
Problem Description
In the current digital age, the amount of natural language text that is available is increasing every day. There is probably an answer to every question is some form of unstructured data. However, the complexity of natural language makes it very difficult to extract information from this text. This project focuses on smaller set of “entity relations” such as “how many people were affected by an epidemic” or “which player was injured in that match” or “what is the main purpose of that rocket launch” and so on.
This project focuses specifically on ten templates and how we can extract information from unstructured text into these templates. The unstructured text that we would be using are from various news articles. The templates that we use are as follows:
 
Awards(Award_name, Recipient, Field, Date)
Acquisition(Buyer, Seller, Product, Price)
killing/murder(Victim, perpetrator, location, Instrument)
injury(player_name, team, type_of_injury, time_to_recover)
Disaster(Type, Location, Country, year) 
Diseases(Name, Location, Victims/casualties,Causes)
kidnap(Victim, perpetrator, location, date, ransom)
Transfers(Player, Transfer team, Amount, time)
Phone(company,model,date,location)
Scandals(person, accusation, Victim, Proved/alleged) 
 
Proposed Solution
For each sentence/paragraph we find entities based on characteristic of the sentence such as Parts of speech tags, hypernyms, hyponyms, meronyms, holonyms and dependency parse. We identify the template based on certain keyword and synonyms. Once we have identified the template, we chunk the sentence to get the features for that template.

Implementation Details
The following tasks were performed:
1. 	Create a set of information templates:
At least 10 information templates
At least 40 information properties
2. 	Create a corpus of natural language statements:
3. 	Implement a deeper NLP pipeline to extract the following NLP based features from the natural language statements:
Tokenize the articles into paragraphs and sentences
Lemmatize the words to extract lemmas as features
Part-of-speech (POS) tag the words to extract POS tag features
Perform dependency parsing to get subjects
Using hypernyms, hyponyms, meronyms, and holonyms to identify entities
4. 	Implement a combination of statistical and heuristic based approach to extract filled information templates from the corpus of natural language statements.

Programming Tools
The following tools were used:
NLTK
Spacy
WordNet

Architectural Diagram

The figure shows the architecture we used for extracting templates. We begin by processing the document into sentences/paragraphs. Each sentence is further subdivided into words using a tokenizer. Each sentence is also tagged with part-of-speech tags and pre-defined entities. We also define custom entities to recognize certain feature. Finally we try to extract relations between entities and fill the information templates.
 
Result and Error Analysis
Accuracy is measured by the number of features picked up the template by the actual number of features that should be detected.



Template 1:
killing(Victim, perpetrator, location, Instrument, Date)
Example:
The bullet responsible for killing Ron Helus from Ventura County during November's mass shooting at the Borderline Bar & Grill was fired by Ian David Long, authorities said Friday.Ron Helus responded to the scene after Ian david Long stormed into the Thousand Oaks bar Nov. 7 and sprayed the crowd with gunfire, killing 12 people with his .45-caliber semi-automatic pistol.

Killing(Ron Helus, Ian david Long, the Borderline Bar & Grill The thousand oaks Ventura County, .45-caliber semi-automatic pistol, Friday Nov.7) 

Template 2:
Acquisition(Buyer, Seller, Product, Price)

Rather than proceed with an imminent initial public offering at a possible valuation of around $4.5 billion, the market-analytics company Qualtrics is selling itself to the German software giant SAP for $8 billion in cash.

Acquisition(software giant SAP, Qualtric, market-analytics, $8 billion)

Template 3:
Awards(Award_name, Recipient, Field, Date)

Now celebrating its 32nd year, the Edison Awards, recognized as the world’s foremost innovation award, announced the 2019 Edison Achievement Award honoree is Ginni Rometty, Chairman, President and Chief Executive Officer of IBM for innovation.

Awards(Edison Achievement, Ginni Rometty, innovation, May 2019)

Template 4:
Scandals(Person, accusation, Victim, Proved/alleged)
Tambor was accused of sexual harrasment by his former assistant "Transparent" actress Trace Lysette and was fired from the series.

Scandals(Tambor, sexual harassment,Van Barnes and “Transparent” actress Trace Lysette, -)
Template 5:
Diseases(Name, location, Victims/Casualities, Causes, Date)

Yemen, a country ravaged by two years of intense conflict, is experiencing a rapidly spreading cholera epidemic. According to the World Health Organization (WHO) and UNICEF, as of Wednesday (June 7) the number of suspected cases of the acute, infectious diarrheal illness has reached 101,820, with 791 deaths.

Diseases(cholera, Yemen, 101,820 791, infectious diarrheal illness, June 7)

Template 6:
Disaster(Type, Location, Country, year) 

The 1931 China floods or the 1931 Yangtze-Huai River floods were a series of devastating floods that occurred in the Republic of China. 

Disaster(floods, Yangtze-Huai River, China, 1931)

Template 7:
injury(player_name, team, type_of_injury, time_to_recover)

Arsenal centre-back Rob Holding has been ruled out for up to nine months after he ruptured the anterior cruciate ligament in his left knee on Wednesday.

injury(Rob Holding, Arsenal, anterior cruciate ligament, nine months)

Template 8:
kidnap(Victim, perpetrator, location, date, ransom)

The South African teenager who was kidnapped by unknown men demanding a $120,000 ransom in bitcoins has been found alive, police say.
Katlego Marite, 13, was taken by three men in a car as he played with two friends near his home in the eastern province of Mpumalanga on Sunday.

kidnap(Katlego Marite, three men, eastern province of Mpumalanga, Sunday, $120,000 )

Template 9:
Transfers(Player, Transfer team, Amount, time)
Ronaldo agrees to four-year, $154-million contract with Juventus

Transfer(Ronaldo, Juventus, $154-million, four-year)
Template 10:
Phone(company,model,date,location)
Apple is widely expected to unveil the iphone 10 at next year's Mobile Congress at Canada, which takes place between 25 and 28 February.

Phone(Apple, iphone10, 25 and 28 February, Canada)


Template
Accuracy
Awards
0.46
Disease
0.59
Disaster
0.40
Works
0.45
Scandal
0.32
Acquisition
0.49
Killing
0.69
Injury
0.59
Phone
0.67
Transfers
0.45

Problems Faced
The following problems were faced:
Generating meaningful templates for data that haven’t already been tabulated.
Collecting a reasonable large and diverse corpus so that most of the test cases are met.
Defining Custom entities for each template. For example, detecting “instrument” entity for “murder” template.
Finding complex relation between entities. For example, detecting which “person” entity is the perpetrator.
Identifying interrelated sentences to get information spread across sentences.

Pending Issues
Extracting information spread across multiple sentences or paragraph. 
Issues when a sentence/article matches more than one template.

Potential Improvements
Identifying Discourse Knowledge
