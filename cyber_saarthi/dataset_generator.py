import json
import os
import random
from pathlib import Path
from typing import List, Dict


CYBER_LAWS_DATA = [
    {
        "instruction": "What is Section 43 of the IT Act 2000?",
        "input": "",
        "output": "Section 43 of the Information Technology Act, 2000 deals with penalty and compensation for damage to computer, computer system, etc. It states that if any person without permission of the owner or any other person in charge of a computer, computer system or computer network: (1) accesses or secures access to such computer; (2) downloads, copies or extracts any data; (3) introduces or causes to be introduced any computer contaminant or computer virus; (4) damages or causes to be damaged any computer system or data; (5) disrupts or causes disruption of any computer system; (6) denies or causes denial of access to any person authorized to access the computer; or (7) provides any assistance to facilitate unauthorized access or downloading of data, then they shall be liable to pay damages by way of compensation to the affected person."
    },
    {
        "instruction": "What are the penalties under Section 43 of the IT Act?",
        "input": "",
        "output": "Under Section 43 of the IT Act 2000, the penalties are primarily compensation-based rather than criminal punishment. The person who commits unauthorized access or damage to computer systems is liable to pay damages by way of compensation to the person affected. The compensation amount is determined based on the extent of damage caused, loss suffered, or wrongful gain made. This is a civil liability provision, not a criminal offense provision."
    },
    {
        "instruction": "What activities are prohibited under Section 43?",
        "input": "",
        "output": "Section 43 prohibits the following activities without permission: 1) Accessing or securing access to a computer, computer system or network; 2) Downloading, copying or extracting any data, computer database or information; 3) Introducing computer contaminants or viruses; 4) Damaging or causing damage to any computer, computer system, network, data, database or software; 5) Disrupting or causing disruption to any computer system; 6) Denying or causing denial of access to authorized users; 7) Providing assistance to facilitate any of the above unauthorized activities."
    },
    
    {
        "instruction": "What is Section 43A of the IT Act about?",
        "input": "",
        "output": "Section 43A of the IT Act 2000 deals with compensation for failure to protect data. It mandates that any body corporate that possesses, deals with, or handles sensitive personal data or information in a computer resource which it owns, controls or operates, and is negligent in implementing and maintaining reasonable security practices and procedures, causing wrongful loss or wrongful gain to any person, shall be liable to pay damages by way of compensation to the person so affected. This section is crucial for data protection and privacy compliance in India."
    },
    {
        "instruction": "What constitutes sensitive personal data under the IT Act?",
        "input": "",
        "output": "Under the IT Act 2000 and the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011, sensitive personal data includes: 1) Passwords; 2) Financial information such as bank accounts, credit/debit card details; 3) Physical, physiological and mental health condition; 4) Sexual orientation; 5) Medical records and history; 6) Biometric information; 7) Any detail relating to the above as provided to body corporate for providing service; 8) Any information received under the above by body corporate for processing or storage. Organizations handling such data must implement reasonable security practices."
    },
    {
        "instruction": "What are reasonable security practices under Section 43A?",
        "input": "",
        "output": "Reasonable security practices under Section 43A refer to security practices and procedures designed to protect sensitive personal data from unauthorized access, damage, use, modification, disclosure or impairment. This includes: 1) A comprehensive documented information security programme and policies; 2) Implementing security standards such as ISO/IEC 27001; 3) Encryption of sensitive data; 4) Access controls and authentication mechanisms; 5) Regular security audits and vulnerability assessments; 6) Incident response procedures; 7) Employee training on data protection. Organizations must also comply with the IT (Reasonable Security Practices) Rules, 2011."
    },
    
    {
        "instruction": "What is Section 66 of the IT Act?",
        "input": "",
        "output": "Section 66 of the IT Act 2000 deals with computer-related offenses. It states that if any person dishonestly or fraudulently does any act referred to in Section 43, they shall be punishable with imprisonment for a term which may extend to three years or with fine which may extend to five lakh rupees, or with both. Essentially, Section 66 provides criminal penalties for the acts defined in Section 43 when committed dishonestly or fraudulently, making it a cognizable and non-bailable offense."
    },
    {
        "instruction": "What is the difference between Section 43 and Section 66?",
        "input": "",
        "output": "The key difference between Section 43 and Section 66 is: Section 43 is a civil liability provision that deals with compensation for unauthorized access or damage to computer systems. The remedy is monetary compensation to the affected party. Section 66, on the other hand, is a criminal provision that punishes the same acts when committed dishonestly or fraudulently. It prescribes imprisonment up to 3 years or fine up to 5 lakh rupees or both. So Section 43 focuses on civil remedies while Section 66 provides for criminal prosecution."
    },
    
    {
        "instruction": "What is Section 66B of the IT Act?",
        "input": "",
        "output": "Section 66B of the IT Act 2000 deals with punishment for dishonestly receiving stolen computer resource or communication device. It states that whoever dishonestly receives or retains any stolen computer resource or communication device knowing or having reason to believe the same to be stolen computer resource or communication device, shall be punished with imprisonment of either description for a term which may extend to three years or with fine which may extend to rupees one lakh or with both."
    },
    
    {
        "instruction": "What is identity theft under the IT Act?",
        "input": "",
        "output": "Identity theft is defined under Section 66C of the IT Act 2000. It states that whoever fraudulently or dishonestly makes use of the electronic signature, password or any other unique identification feature of any other person, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to rupees one lakh. This covers unauthorized use of someone else's digital identity credentials."
    },
    {
        "instruction": "What are the penalties for identity theft in India?",
        "input": "",
        "output": "Under Section 66C of the IT Act 2000, the penalties for identity theft (fraudulent or dishonest use of another person's electronic signature, password, or unique identification) are: imprisonment of either description for a term which may extend to 3 years, AND a fine which may extend to Rs. 1 lakh. This is a cognizable and bailable offense, meaning police can arrest without warrant but the accused can get bail."
    },
    {
        "instruction": "Give me an example of identity theft under Section 66C",
        "input": "",
        "output": "An example of identity theft under Section 66C would be: A person fraudulently obtains someone else's email credentials and uses them to send emails pretending to be that person, perhaps to defraud their contacts or damage their reputation. Another example would be using someone's digital signature without authorization to sign documents or contracts. Using another person's social media passwords to impersonate them online would also constitute identity theft under this section."
    },
    
    {
        "instruction": "What is Section 66D of the IT Act?",
        "input": "",
        "output": "Section 66D of the IT Act 2000 deals with punishment for cheating by personation using computer resources. It states that whoever, by means of any communication device or computer resource, cheats by personation, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to one lakh rupees. This covers online fraud where someone impersonates another person to cheat or deceive."
    },
    {
        "instruction": "What is the difference between Section 66C and 66D?",
        "input": "",
        "output": "The difference between Section 66C and 66D is: Section 66C (identity theft) deals specifically with fraudulent use of someone's electronic signature, password, or unique identification features. Section 66D (cheating by personation) is broader and covers cheating by impersonating another person using any communication device or computer resource. 66C focuses on unauthorized use of credentials, while 66D focuses on the act of impersonation for the purpose of cheating. Both carry similar penalties of up to 3 years imprisonment and fine up to Rs. 1 lakh."
    },
    
    {
        "instruction": "What is Section 66E of the IT Act?",
        "input": "",
        "output": "Section 66E of the IT Act 2000 deals with punishment for violation of privacy. It states that whoever intentionally or knowingly captures, publishes or transmits the image of a private area of any person without his or her consent, under circumstances violating the privacy of that person, shall be punished with imprisonment which may extend to three years or with fine not exceeding two lakh rupees, or with both. This section protects individuals from unauthorized capture and distribution of private images."
    },
    {
        "instruction": "What constitutes privacy violation under Section 66E?",
        "input": "",
        "output": "Under Section 66E, privacy violation occurs when someone: 1) Intentionally or knowingly captures, publishes, or transmits an image of a private area of any person; 2) Does so without that person's consent; 3) Under circumstances that violate the privacy of that person. 'Private area' typically means parts of the body or circumstances where a person would have a reasonable expectation of privacy. This includes unauthorized photography, video recording, or distribution of such content without consent, especially in private settings."
    },
    
    {
        "instruction": "What is cyber terrorism under the IT Act?",
        "input": "",
        "output": "Cyber terrorism is defined under Section 66F of the IT Act 2000. It covers acts of accessing or attempting to access a computer resource without authorization with the intent to threaten the unity, integrity, security, or sovereignty of India or to strike terror in the people. Such acts may include: 1) Denying or causing denial of access to authorized personnel; 2) Attempting to penetrate or access a computer resource without authorization; 3) Introducing contaminants or viruses; 4) Actions that may cause death or injuries to persons or damage to property; 5) Disruption of essential supplies or services. The punishment is imprisonment which may extend to imprisonment for life."
    },
    {
        "instruction": "What are the penalties for cyber terrorism in India?",
        "input": "",
        "output": "Under Section 66F of the IT Act 2000, cyber terrorism carries the most severe penalties. The punishment is imprisonment which may extend to imprisonment for life. This makes it one of the most serious offenses under the IT Act. Cyber terrorism involves unauthorized access to computer resources with intent to threaten India's unity, integrity, security, or sovereignty, or to strike terror in people. It is a non-bailable offense and investigations are typically conducted by specialized agencies like the National Investigation Agency (NIA)."
    },
    
    {
        "instruction": "What is Section 67 of the IT Act?",
        "input": "",
        "output": "Section 67 of the IT Act 2000 deals with punishment for publishing or transmitting obscene material in electronic form. It states that whoever publishes or transmits or causes to be published or transmitted in electronic form, any material which is lascivious or appeals to the prurient interest or tends to deprave and corrupt persons, shall be punished on first conviction with imprisonment of either description for a term which may extend to three years and with fine which may extend to five lakh rupees, and in the event of second or subsequent conviction with imprisonment of either description for a term which may extend to five years and with fine which may extend to ten lakh rupees."
    },
    {
        "instruction": "What is the punishment for publishing obscene content online?",
        "input": "",
        "output": "Under Section 67 of the IT Act, the punishment for publishing or transmitting obscene material in electronic form is: First conviction - imprisonment up to 3 years AND fine up to Rs. 5 lakhs. Second or subsequent conviction - imprisonment up to 5 years AND fine up to Rs. 10 lakhs. The offense covers publishing, transmitting, or causing to publish/transmit material that is lascivious, appeals to prurient interest, or tends to deprave and corrupt persons."
    },
    
    {
        "instruction": "What is Section 67A of the IT Act?",
        "input": "",
        "output": "Section 67A of the IT Act 2000 deals with punishment for publishing or transmitting material containing sexually explicit acts in electronic form. It is more specific than Section 67 and covers material that contains sexually explicit acts or conduct. First conviction carries imprisonment up to 5 years and fine up to Rs. 10 lakhs. Second or subsequent conviction carries imprisonment up to 7 years and fine up to Rs. 10 lakhs. This section specifically targets pornographic content in electronic form."
    },
    {
        "instruction": "What is the difference between Section 67 and 67A?",
        "input": "",
        "output": "The difference between Section 67 and 67A is: Section 67 deals with obscene material that is lascivious or appeals to prurient interest - this is broader and more subjective. Section 67A specifically deals with material containing sexually explicit acts or conduct - this is more specific and focused on pornographic content. Section 67A carries harsher penalties (up to 5 years for first conviction vs 3 years, and up to 7 years for subsequent convictions vs 5 years) because it deals with more explicit content."
    },
    
    {
        "instruction": "What is Section 67B of the IT Act?",
        "input": "",
        "output": "Section 67B of the IT Act 2000 specifically addresses child pornography. It punishes publishing, transmitting, creating, collecting, seeking, browsing, downloading, advertising, promoting, exchanging or distributing material depicting children in sexually explicit acts or conduct in electronic form. The punishment on first conviction is imprisonment up to 5 years and fine up to Rs. 10 lakhs. For second or subsequent conviction, imprisonment up to 7 years and fine up to Rs. 10 lakhs. This section provides strong protection for children from sexual exploitation online."
    },
    
    {
        "instruction": "What is Section 69 of the IT Act?",
        "input": "",
        "output": "Section 69 of the IT Act 2000 gives the Central Government or a State Government or any of its authorized officers the power to issue directions for interception, monitoring, or decryption of any information transmitted through any computer resource. This can be done in the interest of India's sovereignty, integrity, defense, security, friendly relations with foreign countries, public order, or for preventing incitement to cognizable offenses or for investigation of offenses. The subscriber or intermediary must assist and comply with such directions, and failure to do so is punishable with imprisonment up to 7 years and fine."
    },
    {
        "instruction": "Can the government intercept my online communications?",
        "input": "",
        "output": "Yes, under Section 69 of the IT Act 2000, the Central or State Government can issue directions for interception, monitoring, or decryption of information transmitted through computer resources, but only under specific circumstances: 1) In the interest of India's sovereignty, integrity, defense, or security; 2) Friendly relations with foreign countries; 3) Public order; 4) Preventing incitement to cognizable offenses; 5) Investigation of offenses. However, such interception must follow proper procedures under the IT (Procedure and Safeguards for Interception, Monitoring and Decryption of Information) Rules, 2009, which provide certain safeguards and oversight mechanisms."
    },
    
    {
        "instruction": "What is Section 70 of the IT Act?",
        "input": "",
        "output": "Section 70 of the IT Act 2000 deals with protected systems. It empowers the Central Government to declare certain computer resources as protected systems by notification in the Official Gazette. These are critical information infrastructure systems whose protection is essential. Unauthorized access to such protected systems is punishable with imprisonment up to 10 years and fine. The government can specify security measures and procedures for accessing these systems. This section helps protect critical national infrastructure like power grids, financial systems, telecommunications networks, etc."
    },
    {
        "instruction": "What is the punishment for accessing protected systems?",
        "input": "",
        "output": "Under Section 70 of the IT Act, unauthorized access to a protected system (computer resources declared as protected by the Central Government) is punishable with imprisonment up to 10 years and fine. This is one of the highest penalties under the IT Act, reflecting the critical importance of protected systems to national security and essential services. Protected systems typically include critical information infrastructure such as power grids, financial systems, government networks, telecommunications infrastructure, etc."
    },
    
    {
        "instruction": "What is Section 72 of the IT Act?",
        "input": "",
        "output": "Section 72 of the IT Act 2000 deals with penalty for breach of confidentiality and privacy. It states that if any person who, in pursuance of any powers conferred under the Act or rules, has secured access to any electronic record, book, register, correspondence, information, document or other material without the consent of the person concerned, discloses such material to any other person, they shall be punished with imprisonment up to 2 years or fine up to Rs. 1 lakh or both. However, disclosure is permitted if required by law or for cybersecurity purposes."
    },
    {
        "instruction": "When can information be disclosed under Section 72?",
        "input": "",
        "output": "Under Section 72, information obtained through powers under the IT Act can be disclosed without penalty in the following circumstances: 1) When disclosure is for the purposes of the IT Act itself; 2) When disclosure is required under any other law that is currently in force; 3) When disclosure is necessary to cybersecurity or for investigation or prosecution of offenses. Any other disclosure without the consent of the person concerned would constitute breach of confidentiality and is punishable with imprisonment up to 2 years or fine up to Rs. 1 lakh or both."
    },
    
    {
        "instruction": "What is Section 72A of the IT Act?",
        "input": "",
        "output": "Section 72A of the IT Act 2000 specifically addresses punishment for disclosure of information in breach of lawful contract. It applies when a service provider discloses personal information of someone in breach of a lawful contract, without that person's consent, causing wrongful loss or wrongful gain. The punishment is imprisonment up to 3 years or fine up to Rs. 5 lakhs or both. This section strengthens privacy protection by making it a criminal offense to violate contractual privacy obligations."
    },
    
    {
        "instruction": "Does the IT Act apply to offenses committed outside India?",
        "input": "",
        "output": "Yes, under Section 75 of the IT Act 2000, the Act has extra-territorial application. It applies to any offense or contravention committed outside India by any person if: 1) The act or conduct constituting the offense or contravention involves a computer, computer system, or computer network located in India; OR 2) The person who committed the offense holds an Indian nationality. This means that even if you're physically outside India, if the crime involves a computer system in India or you're an Indian citizen, you can be prosecuted under the IT Act."
    },
    {
        "instruction": "What is extra-territorial jurisdiction under the IT Act?",
        "input": "",
        "output": "Extra-territorial jurisdiction under Section 75 of the IT Act means that the Act can be applied to offenses committed outside India's physical borders. The key conditions are: 1) The offense involves a computer, computer system, or computer network located in India, regardless of where the offender is located; OR 2) The offender is an Indian citizen, regardless of where the offense was committed. For example, if someone in another country hacks into a computer server located in India, they can be prosecuted under the IT Act even though they never entered India physically."
    },
    
    {
        "instruction": "What is Section 79 of the IT Act?",
        "input": "",
        "output": "Section 79 of the IT Act 2000 deals with intermediary liability exemption. It provides that intermediaries (like internet service providers, social media platforms, hosting services) shall not be liable for any third-party information, data, or communication link made available or hosted by them, provided: 1) Their function is limited to providing access to a communication system or transmitting information; 2) They don't initiate the transmission, select the receiver, or select/modify the information; 3) They observe due diligence and follow guidelines prescribed by the government; 4) They don't have actual knowledge of illegal content, or upon obtaining knowledge or being notified, they act expeditiously to remove or disable access to that content."
    },
    {
        "instruction": "Are social media platforms liable for user content?",
        "input": "",
        "output": "Under Section 79 of the IT Act and the IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021, social media platforms (intermediaries) have conditional exemption from liability for third-party content. They are NOT liable if they: 1) Act only as intermediaries (don't create or modify content); 2) Observe due diligence; 3) Follow intermediary guidelines; 4) Don't have actual knowledge of illegal content; 5) Remove or disable access to illegal content expeditiously upon receiving actual knowledge or being notified. However, they lose this exemption if they fail to observe due diligence, don't follow guidelines, or don't act promptly to remove illegal content after being notified."
    },
    
    {
        "instruction": "What is hacking according to Indian cyber law?",
        "input": "",
        "output": "Under Indian cyber law (IT Act 2000), hacking is not explicitly defined but is covered under various sections. It generally means unauthorized access to computer systems, networks, or data. Section 43 provides civil liability for unauthorized access, while Section 66 makes it a criminal offense when done dishonestly or fraudulently. Hacking activities include: unauthorized access to systems, data theft, introducing viruses, disrupting services, or extracting information without permission. The punishment can range from compensation (Section 43) to imprisonment up to 3 years for computer-related offenses (Section 66)."
    },
    {
        "instruction": "What are the penalties for hacking in India?",
        "input": "",
        "output": "Penalties for hacking in India depend on the specific offense: 1) Under Section 43 - Civil liability with compensation to the affected party; 2) Under Section 66 - Criminal offense with imprisonment up to 3 years or fine up to Rs. 5 lakhs or both for dishonest/fraudulent computer-related offenses; 3) Under Section 66B - Imprisonment up to 3 years or fine up to Rs. 1 lakh for receiving stolen computer resources; 4) Under Section 70 - Imprisonment up to 10 years for unauthorized access to protected systems; 5) Under Section 66F - Life imprisonment if hacking is done with intent to threaten national security (cyber terrorism)."
    },
    
    {
        "instruction": "What are the data protection laws in India?",
        "input": "",
        "output": "India's data protection framework currently consists of: 1) Section 43A of the IT Act 2000 - Requires body corporates to implement reasonable security practices for sensitive personal data; 2) IT (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011 - Defines sensitive personal data and prescribes security requirements; 3) Section 72A - Criminalizes disclosure of personal information in breach of contract; 4) Various sectoral regulations like RBI guidelines for financial data, TRAI regulations for telecom data. Note: The Digital Personal Data Protection Act, 2023 has been passed and will provide a comprehensive data protection framework once implemented."
    },
    {
        "instruction": "What are the obligations of companies handling personal data?",
        "input": "",
        "output": "Under the IT Act 2000 and related rules, companies (body corporates) handling sensitive personal data must: 1) Obtain consent before collecting sensitive personal data; 2) Implement and maintain reasonable security practices and procedures (like ISO 27001 or equivalent); 3) Have a documented privacy policy; 4) Collect data only for lawful purposes; 5) Not retain data longer than required; 6) Allow individuals to review and correct their information; 7) Not disclose information without consent except as required by law; 8) Ensure data is transferred only to countries with adequate protection or with consent. Failure to protect data can result in liability under Section 43A."
    },
    
    {
        "instruction": "What are cybersecurity best practices for individuals?",
        "input": "",
        "output": "Key cybersecurity best practices for individuals include: 1) Use strong, unique passwords for each account and enable two-factor authentication; 2) Keep software, operating systems, and antivirus updated; 3) Be cautious of phishing emails and suspicious links; 4) Use secure networks (avoid public Wi-Fi for sensitive transactions); 5) Regularly backup important data; 6) Be careful about what you share on social media; 7) Use encryption for sensitive communications; 8) Monitor bank and credit card statements regularly; 9) Use privacy settings on social media and apps; 10) Be aware of online scams and report suspicious activities to cybercrime.gov.in or local cyber cell."
    },
    {
        "instruction": "What are cybersecurity best practices for organizations?",
        "input": "",
        "output": "Cybersecurity best practices for organizations include: 1) Implement comprehensive information security policies and procedures; 2) Comply with relevant standards (ISO 27001, NIST framework); 3) Conduct regular security audits and vulnerability assessments; 4) Implement access controls and authentication mechanisms; 5) Encrypt sensitive data (in transit and at rest); 6) Have incident response and disaster recovery plans; 7) Provide regular cybersecurity training to employees; 8) Implement network security measures (firewalls, IDS/IPS); 9) Regular patch management and software updates; 10) Conduct background checks for employees with access to sensitive data; 11) Implement data loss prevention (DLP) solutions; 12) Maintain compliance with IT Act 2000, especially Sections 43A and 72A."
    },
    
    {
        "instruction": "How do I report a cybercrime in India?",
        "input": "",
        "output": "To report a cybercrime in India, you can: 1) File a complaint online at the National Cybercrime Reporting Portal (cybercrime.gov.in); 2) Report to your local cyber cell or police station; 3) For women and children related cybercrimes, report at cybercrime.gov.in which has a dedicated section; 4) Call the National Cybercrime Helpline at 1930; 5) For financial fraud, immediately inform your bank and report to cybercrime portal; 6) Preserve all evidence including screenshots, emails, transaction details, URLs, etc. Time is crucial in cybercrime cases, so report as soon as possible. The complaint can be filed from anywhere in India, regardless of where the crime occurred."
    },
    {
        "instruction": "What information should I provide when reporting a cybercrime?",
        "input": "",
        "output": "When reporting a cybercrime, provide: 1) Your complete details (name, contact, address); 2) Detailed description of the incident including date, time, and sequence of events; 3) Details of the suspect if known (name, email, phone, social media handles, URLs); 4) Evidence: screenshots of messages, emails, transaction details, bank statements, URLs of websites/profiles, chat logs; 5) Financial details if money is involved (transaction IDs, amounts, account numbers); 6) Any previous communication with the suspect; 7) Details of any financial or other loss suffered; 8) Names and contacts of any witnesses. Preserve all digital evidence and don't delete anything until advised by investigating officers."
    },
    
    {
        "instruction": "What is CERT-In?",
        "input": "",
        "output": "CERT-In (Indian Computer Emergency Response Team) is the national nodal agency for responding to computer security incidents in India. It was established under Section 70B of the IT Act 2000. CERT-In's responsibilities include: 1) Collecting, analyzing and disseminating information on cyber incidents; 2) Forecasting and issuing alerts on cybersecurity incidents; 3) Providing emergency measures for handling cybersecurity incidents; 4) Coordinating cyber incident response activities; 5) Issuing guidelines and advisories on information security practices; 6) Conducting cybersecurity drills and training. Organizations and service providers are required to report cybersecurity incidents to CERT-In as per the IT Act rules."
    },
    {
        "instruction": "What incidents must be reported to CERT-In?",
        "input": "",
        "output": "Under the IT (The Indian Computer Emergency Response Team and Manner of Performing Functions and Duties) Rules, 2013 and subsequent amendments, service providers, intermediaries, data centers, and body corporates must report the following incidents to CERT-In within 6 hours: 1) Targeted scanning/probing of critical networks/systems; 2) Compromise of critical systems/information; 3) Unauthorized access to IT systems/data; 4) Defacement of websites; 5) Malicious code attacks (virus, worm, trojan, ransomware); 6) Attacks on servers (database, mail, DNS); 7) Identity theft, spoofing, phishing; 8) Denial of Service (DoS/DDoS) attacks; 9) Attacks on critical infrastructure; 10) Data breaches and leaks. Organizations must also maintain IT system logs for 180 days."
    },
]

ADDITIONAL_TOPICS = [
    "What constitutes a computer under the IT Act?",
    "What is a computer system according to Indian law?",
    "What is a computer network under the IT Act?",
    "What is the role of digital signatures in Indian cyber law?",
    "Are electronic records legally valid in India?",
    "What is the significance of the IT Act 2000?",
    "When was the IT Act 2000 enacted?",
    "What are the main amendments to the IT Act?",
    "What is the IT Amendment Act 2008?",
    "What is a cyber cafe regulation under the IT Act?",
    "What are the duties of intermediaries under the IT Act?",
    "What is the role of the Controller of Certifying Authorities?",
    "What are Certifying Authorities under the IT Act?",
    "What is an electronic signature?",
    "What is the difference between digital and electronic signatures?",
    "What is phishing?",
    "What is ransomware?",
    "What is malware?",
    "What is a DDoS attack?",
    "What is social engineering in cybersecurity?",
    "What is spear phishing?",
    "What is a man-in-the-middle attack?",
    "What is SQL injection?",
    "What is cross-site scripting (XSS)?",
    "What is zero-day vulnerability?",
    "What is encryption?",
    "What is two-factor authentication?",
    "What is a VPN and how does it protect privacy?",
    "What is the dark web?",
    "What is cryptocurrency fraud?",
    "What is online banking fraud?",
    "What is UPI fraud?",
    "What is SIM swapping?",
    "What is vishing?",
    "What is smishing?",
    "What should I do if I receive a suspicious email?",
    "How can I protect my social media accounts?",
    "What is cyberbullying under Indian law?",
    "What is online harassment?",
    "What are the laws against online defamation in India?",
    "What is sextortion?",
    "How to report online child abuse?",
    "What is the POCSO Act in relation to cybercrimes?",
    "What are cyber laws for e-commerce?",
    "What is the liability of e-commerce platforms?",
    "What are the consumer protection laws for online transactions?",
    "What is digital arrest scam?",
    "What are<truncated>",
    "What is the punishment for online fraud?",
    "What is the punishment for credit card fraud?",
    "What is ATM fraud?",
    "How to protect against online scams?",
    "What is business email compromise?",
    "What is CEO fraud?",
    "What security measures should I take for online banking?",
    "What is the National Cyber Security Policy?",
    "What is the role of police in cybercrime investigation?",
    "Can I file an FIR online for cybercrimes?",
    "What is the jurisdiction for cybercrimes in India?",
    "What evidence is needed for cybercrime prosecution?",
    "What is digital forensics?",
    "What is the role of ISPs in preventing cybercrimes?",
    "What are blocking rights under the IT Act?",
    "Can the government block websites in India?",
    "What is the safe harbor provision for intermediaries?",
    "What are the due diligence requirements for intermediaries?",
    "What happens if I don't comply with CERT-In directions?",
    "What is the punishment for non-compliance with government directions under Section 69?",
    "What are the IT Rules 2021?",
    "What is the Intermediary Guidelines and Digital Media Ethics Code?",
    "What is the grievance redressal mechanism for social media?",
    "Who is a Grievance Officer under IT Rules?",
    "What is the role of Chief Compliance Officer?",
    "What are significant social media intermediaries?",
    "What is end-to-end encryption?",
    "Can the government ask for decryption of messages?",
    "What is the right to be forgotten in India?",
    "How long can companies retain personal data?",
    "What is consent for data processing?",
    "What is data localization?",
    "Where should Indian user data be stored?",
    "What is cross-border data transfer?",
    "What is a data breach?",
    "What should companies do in case of a data breach?",
    "Must data breaches be reported?",
    "What is the punishment for data breach?",
    "What is the role of Data Protection Officer?",
    "What is privacy by design?",
    "What is anonymization of data?",
    "What is pseudonymization?",
    "What are the privacy implications of AI?",
    "What is automated decision making?",
    "What is profiling under data protection laws?",
    "What are cookies and their legal implications?",
    "Do websites need privacy policies?",
    "What should a privacy policy contain?",
    "What is the legal validity of terms and conditions?",
    "What is clickwrap agreement?",
    "What is browsewrap agreement?",
    "What is electronic contract?",
    "Are WhatsApp messages admissible as evidence?",
    "Are emails admissible as evidence in court?",
    "What is the Indian Evidence Act provision for electronic records?",
    "What is Section 65B of the Indian Evidence Act?",
    "What is a certificate under Section 65B?",
    "How to authenticate electronic evidence?",
    "What is blockchain technology?",
    "What are the legal implications of blockchain in India?",
    "What is cryptocurrency regulation in India?",
    "Are cryptocurrencies legal in India?",
    "What is smart contract?",
    "What are NFTs and their legal status?",
    "What is Internet of Things (IoT) security?",
    "What are the cybersecurity risks of IoT?",
    "What is cloud computing?",
    "What are the security concerns with cloud computing?",
    "Who is responsible for cloud data security?",
    "What is bring your own device (BYOD) policy?",
    "What are the security risks of remote work?",
    "What is insider threat?",
    "What is privilege escalation?",
    "What is backdoor in cybersecurity?",
    "What is rootkit?",
    "What is keylogger?",
    "What is botnet?",
    "What is command and control server?",
    "What is advanced persistent threat (APT)?",
    "What is threat intelligence?",
    "What is security information and event management (SIEM)?",
    "What is penetration testing?",
    "What is vulnerability assessment?",
    "What is red team vs blue team?",
    "What is bug bounty program?",
    "What is responsible disclosure?",
    "What is cybersecurity awareness training?",
    "What is security by obscurity?",
    "What is defense in depth?",
    "What is least privilege principle?",
    "What is network segmentation?",
    "What is firewall?",
    "What is intrusion detection system?",
    "What is intrusion prevention system?",
    "What is antivirus vs anti-malware?",
    "What is endpoint protection?",
    "What is email security?",
    "What is spam filtering?",
    "What is DMARC, SPF, and DKIM?",
    "What is web application firewall?",
    "What is SSL/TLS certificate?",
    "What is HTTPS?",
    "What is certificate pinning?",
    "What is public key infrastructure?",
    "What is digital certificate?",
    "What is certificate authority?",
    "What is hash function?",
    "What is salting in password security?",
    "What is password hashing?",
    "What is rainbow table attack?",
    "What is brute force attack?",
    "What is dictionary attack?",
    "What is credential stuffing?",
    "What is session hijacking?",
    "What is clickjacking?",
    "What is CSRF attack?",
    "What is XML external entity attack?",
    "What is server-side request forgery?",
    "What is remote code execution?",
    "What is buffer overflow?",
    "What is race condition vulnerability?",
    "What is OWASP Top 10?",
    "What is secure coding practices?",
    "What is input validation?",
    "What is output encoding?",
    "What is parameterized query?",
    "What is Content Security Policy?",
    "What is the role of HTTP security headers?",
    "What is CORS?",
    "What is same-origin policy?",
    "What is API security?",
    "What is OAuth?",
    "What is JWT token?",
    "What is API key?",
    "What is rate limiting?",
    "What is honeypot in cybersecurity?",
    "What is security audit?",
    "What is compliance audit?",
    "What is ISO 27001?",
    "What is NIST Cybersecurity Framework?",
    "What is PCI DSS?",
    "What is GDPR and does it apply to India?",
    "What is the difference between privacy and security?",
    "What is cyber insurance?",
    "What is incident response plan?",
    "What is disaster recovery plan?",
    "What is business continuity planning?",
    "What is cyber resilience?",
    "What is security awareness?",
    "What is human factor in cybersecurity?",
    "What is supply chain attack?",
    "What is third-party risk management?",
    "What is vendor risk assessment?",
    "What is cyber hygiene?",
    "What is patch management?",
    "What is change management in IT security?",
    "What is configuration management?",
    "What is asset management in cybersecurity?",
    "What is data classification?",
    "What is information lifecycle management?",
    "What is secure disposal of data?",
    "What is data sanitization?",
    "What is degaussing?",
    "What is the 3-2-1 backup rule?",
    "What is air-gapped system?",
    "What is zero trust architecture?",
    "What is microsegmentation?",
    "What is software-defined perimeter?",
    "What is security orchestration and automation?",
    "What is artificial intelligence in cybersecurity?",
    "What is machine learning for threat detection?",
    "What is behavioral analytics?",
    "What is user and entity behavior analytics (UEBA)?",
    "What is deception technology?",
    "What is threat hunting?",
    "What is cyber threat intelligence sharing?",
    "What is information sharing and analysis center (ISAC)?",
    "What is the role of NCIIPC in India?",
    "What is critical information infrastructure?",
    "What are critical sectors under cybersecurity in India?",
    "What is the National Critical Information Infrastructure Protection Centre?",
    "What is the National Cyber Coordination Centre?",
    "What is the National Cyber Security Coordinator?",
    "What is cyber warfare?",
    "What is cyber espionage?",
    "What is hacktivism?",
    "What is state-sponsored hacking?",
    "What is attribution in cyberattacks?",
    "What is the Budapest Convention on Cybercrime?",
    "Is India party to the Budapest Convention?",
    "What is international cooperation in cybercrime?",
    "What is mutual legal assistance in cybercrimes?",
    "What is extradition for cybercrimes?",
    "What is the role of Interpol in cybercrimes?",
    "What is cyber diplomacy?",
    "What are the ethical considerations in cybersecurity?",
    "What is ethical hacking?",
    "What is white hat vs black hat hacker?",
    "What is grey hat hacker?",
    "What is script kiddie?",
    "What is hacking for good?",
    "What certifications are important for cybersecurity professionals?",
    "What is CISSP?",
    "What is CEH (Certified Ethical Hacker)?",
    "What is the career scope in cybersecurity in India?",
    "What skills are needed for cybersecurity?",
    "What is the future of cybersecurity?",
    "What are emerging threats in cybersecurity?",
    "What is quantum computing impact on cybersecurity?",
    "What is post-quantum cryptography?",
    "What is 5G security?",
    "What are the cybersecurity challenges of 5G?",
    "What is edge computing security?",
    "What is container security?",
    "What is Kubernetes security?",
    "What is DevSecOps?",
    "What is shift-left security?",
    "What is security testing in CI/CD pipeline?",
    "What is static application security testing (SAST)?",
    "What is dynamic application security testing (DAST)?",
    "What is interactive application security testing (IAST)?",
    "What is software composition analysis (SCA)?",
    "What is dependency scanning?",
    "What is open source security?",
    "What are the risks of using open source software?",
    "What is software bill of materials (SBOM)?",
    "What is supply chain security for software?",
    "What is the importance of cybersecurity in healthcare?",
    "What is HIPAA equivalent in India for healthcare data?",
    "What are cybersecurity requirements for digital health?",
    "What is telemedicine security?",
    "What are the cybersecurity concerns in smart cities?",
    "What is OT (Operational Technology) security?",
    "What is IT/OT convergence?",
    "What is SCADA security?",
    "What is industrial control system security?",
    "What are the cybersecurity requirements for power sector?",
    "What is cybersecurity for banking sector in India?",
    "What are RBI guidelines on cybersecurity?",
    "What is cyber fraud in UPI?",
    "How to secure mobile banking?",
    "What is payment gateway security?",
    "What is tokenization in payment security?",
    "What is PCI compliance?",
    "What are ATM security requirements?",
    "What is cybersecurity for stock exchanges?",
    "What is insider trading detection?",
    "What are the cybersecurity requirements for telecom sector?",
    "What are TRAI regulations on cybersecurity?",
    "What is telecom fraud?",
    "What is SIM cloning?",
    "What is mobile device management?",
    "What is mobile application security?",
    "What are OWASP Mobile Top 10?",
    "What is app security testing?",
    "What is jailbreaking risks?",
    "What is rooting risks for Android?",
    "What is the security of biometric authentication?",
    "What is liveness detection?",
    "What is spoofing in biometrics?",
    "What is Aadhaar security?",
    "What are the privacy concerns with Aadhaar?",
    "What is the Supreme Court judgment on Aadhaar?",
    "What is eKYC security?",
    "What is digital identity?",
    "What is self-sovereign identity?",
    "What is decentralized identifier?",
    "What is verifiable credentials?",
    "What is the India Stack?",
    "What is DigiLocker security?",
    "What is UPI security?",
    "What is BHIM app security?",
    "What is the security of Aarogya Setu?",
    "What is contact tracing app privacy?",
    "What are the cybersecurity implications of work from home?",
    "What is shadow IT?",
    "What is data exfiltration?",
    "What is data loss prevention?",
    "What is email archiving?",
    "What is eDiscovery?",
    "What is legal hold?",
    "What is forensic readiness?",
    "What is chain of custody in digital evidence?",
    "What is write blocker in digital forensics?",
    "What is disk imaging?",
    "What is memory forensics?",
    "What is network forensics?",
    "What is log analysis?",
    "What is timeline analysis?",
    "What is malware analysis?",
    "What is reverse engineering?",
    "What is sandboxing?",
    "What is virtual machine escape?",
    "What is container escape?",
    "What is the role of cybersecurity in national security?",
    "What is critical infrastructure protection?",
    "What is the National Cyber Security Strategy of India?",
    "What is cyber resilience vs cybersecurity?",
]


def generate_response(question: str) -> str:
    """Generate a response for questions not in the predefined dataset"""
    responses = {
        "What constitutes a computer under the IT Act?": "According to Section 2(1)(i) of the IT Act 2000, 'computer' means any electronic, magnetic, optical or other high-speed data processing device or system which performs logical, arithmetic, and memory functions by manipulations of electronic, magnetic or optical impulses, and includes all input, output, processing, storage, computer software, or communication facilities which are connected or related to the computer in a computer system or computer network.",
        
        "What is a computer system according to Indian law?": "Under Section 2(1)(l) of the IT Act 2000, 'computer system' means a device or collection of devices, including input and output support devices and excluding calculators which are not programmable and capable of being used in conjunction with external files, which contain computer programmes, electronic instructions, input data and output data, that performs logic, arithmetic, data storage and retrieval, communication control and other functions.",
        
        "What is a computer network under the IT Act?": "According to Section 2(1)(j) of the IT Act 2000, 'computer network' means the interconnection of one or more computers or computer systems or communication device through the use of satellite, microwave, terrestrial line, wireless or other communication media and terminals or a complex consisting of two or more interconnected computers or communication device whether or not the interconnection is continuously maintained.",
        
        "What is the role of digital signatures in Indian cyber law?": "Digital signatures under the IT Act 2000 provide legal validity to electronic documents. Section 3 recognizes digital signatures as a method of authentication. A digital signature is created using asymmetric cryptography and ensures: 1) Authentication (verifies the signatory's identity); 2) Integrity (ensures the document hasn't been altered); 3) Non-repudiation (the signatory cannot deny having signed). Digital signatures issued by licensed Certifying Authorities under the Act have the same legal validity as handwritten signatures for most purposes.",
        
        "Are electronic records legally valid in India?": "Yes, Section 4 of the IT Act 2000 gives legal recognition to electronic records. It states that where any law requires information to be in writing or in the typewritten or printed form, such requirement shall be deemed to have been satisfied if the information is rendered or made available in an electronic form and accessible for subsequent reference. However, certain documents like negotiable instruments, powers of attorney, trusts, wills, and contracts for sale of immovable property are excluded from this provision.",
    }
    
    # Return None if question not found - we'll skip it instead of using generic disclaimer
    return responses.get(question, None)


def create_dataset():
    """Create the complete dataset with extensive variations"""
    dataset = CYBER_LAWS_DATA.copy()
    
    # Add the 5 predefined additional topics that have real answers
    for question in ADDITIONAL_TOPICS:
        if question.endswith('...'):
            continue
        response = generate_response(question)
        # Skip questions without real answers (returns None)
        if response is not None:
            dataset.append({
                "instruction": question,
                "input": "",
                "output": response
            })
    
    variations = []
    
    # Create EXTENSIVE variations for ALL items in CYBER_LAWS_DATA (10+ per item)
    for item in CYBER_LAWS_DATA:
        instruction = item["instruction"]
        output = item["output"]
        
        # Extract section number if present
        section_num = None
        if "Section" in instruction:
            try:
                section_num = instruction.split("Section")[1].split()[0].strip()
            except:
                pass
        
        # Variation Set 1: Question format variations
        if "What is" in instruction:
            topic = instruction.replace("What is ", "").replace("?", "")
            
            # Casual/conversational
            variations.append({"instruction": f"Can you explain {topic} in simple terms?", "input": "", "output": output})
            variations.append({"instruction": f"Tell me about {topic}", "input": "", "output": output})
            variations.append({"instruction": f"I want to know about {topic.lower()}", "input": "", "output": output})
            variations.append({"instruction": f"Explain {topic} to me", "input": "", "output": output})
            variations.append({"instruction": f"Help me understand {topic.lower()}", "input": "", "output": output})
            
        if "What are" in instruction:
            topic = instruction.replace("What are ", "").replace("?", "")
            variations.append({"instruction": f"Tell me about {topic.lower()}", "input": "", "output": output})
            variations.append({"instruction": f"Explain {topic.lower()}", "input": "", "output": output})
            variations.append({"instruction": f"Can you list {topic.lower()}?", "input": "", "output": output})
        
        # Variation Set 2: Section-specific formats (if applicable)
        if section_num:
            variations.append({"instruction": f"Explain Section {section_num}", "input": "", "output": output})
            variations.append({"instruction": f"What does Section {section_num} say?", "input": "", "output": output})
            variations.append({"instruction": f"Tell me about Section {section_num}", "input": "", "output": output})
            variations.append({"instruction": f"Describe Section {section_num} of IT Act", "input": "", "output": output})
            variations.append({"instruction": f"Section {section_num} meaning", "input": "", "output": output})
            variations.append({"instruction": f"I need information on Section {section_num}", "input": "", "output": output})
        
        # Variation Set 3: Shortened/casual versions
        if "?" in instruction:
            # Remove question mark, make it a statement
            no_q = instruction.replace("?", "")
            variations.append({"instruction": no_q, "input": "", "output": output})
            
        # Variation Set 4: "How does X work" for technical topics
        if any(word in instruction.lower() for word in ["protection", "security", "practices", "encryption", "authentication"]):
            if "What is" in instruction or "What are" in instruction:
                topic = instruction.replace("What is ", "").replace("What are ", "").replace("?", "")
                variations.append({"instruction": f"How does {topic.lower()} work?", "input": "", "output": output})
                variations.append({"instruction": f"How do {topic.lower()} function?", "input": "", "output": output})
        
        # Variation Set 5: Penalty/punishment-specific questions
        if "penalties" in instruction.lower() or "punishment" in instruction.lower():
            if section_num:
                variations.append({"instruction": f"What happens if I violate Section {section_num}?", "input": "", "output": output})
                variations.append({"instruction": f"Consequences of Section {section_num} violation", "input": "", "output": output})
                variations.append({"instruction": f"Legal consequences under Section {section_num}", "input": "", "output": output})
        
        # Variation Set 6: Example-based questions  
        if "example" not in instruction.lower():
            if section_num:
                topic = instruction.replace(f"Section {section_num}", "").replace("What is", "").replace("?", "").strip()
                if topic:
                    variations.append({"instruction": f"Give me examples of {topic.lower()}", "input": "", "output": output})
                    
        # Variation Set 7: Paraphrased versions
        paraphrases = {
            "What is": ["Define", "Describe", "Meaning of"],
            "What are": ["List", "Describe", "Enumerate"],
            "punishment": ["penalties", "consequences", "legal actions"],
            "deals with": ["covers", "relates to", "addresses"],
        }
        
        for old, new_list in paraphrases.items():
            if old in instruction:
                for new in new_list:
                    new_instruction = instruction.replace(old, new)
                    if new_instruction != instruction:  # Only add if different
                        variations.append({"instruction": new_instruction, "input": "", "output": output})
        
        # Variation Set 8: Scenario/practical questions
        if "identity theft" in instruction.lower():
            variations.append({"instruction": "Someone used my password without permission, what law applies?", "input": "", "output": output})
            variations.append({"instruction": "Unauthorized use of digital credentials punishment", "input": "", "output": output})
            
        if "hacking" in instruction.lower():
            variations.append({"instruction": "Unauthorized computer access penalties", "input": "", "output": output})
            variations.append({"instruction": "What if someone breaks into my computer system?", "input": "", "output": output})
            
        if "data protection" in instruction.lower() or "43A" in instruction:
            variations.append({"instruction": "Company leaked my data, what can I do?", "input": "", "output": output})
            variations.append({"instruction": "Data breach compensation laws India", "input": "", "output": output})
            
        if "privacy" in instruction.lower() and "66E" in instruction:
            variations.append({"instruction": "Someone shared my private images without consent", "input": "", "output": output})
            variations.append({"instruction": "Unauthorized photography laws India", "input": "", "output": output})
            
        if "cybercrime" in instruction.lower() and "report" in instruction.lower():
            variations.append({"instruction": "Where to report cyber fraud?", "input": "", "output": output})
            variations.append({"instruction": "How to file cybercrime complaint?", "input": "", "output": output})
            variations.append({"instruction": "Steps to report online crime", "input": "", "output": output})
    
    # Variation Set 9: Comparative questions for key sections
    comparisons = [
        ("Section 43", "Section 66", "What is the difference between Section 43 and 66?"),
        ("Section 66C", "Section 66D", "What is the difference between Section 66C and 66D?"),
        ("Section 67", "Section 67A", "What is the difference between Section 67 and 67A?"),
    ]
    
    for sec1, sec2, question in comparisons:
        # Find the comparison answer if it exists in CYBER_LAWS_DATA
        for item in CYBER_LAWS_DATA:
            if sec1 in item["instruction"] and sec2 in item["instruction"] and "difference" in item["instruction"].lower():
                comp_output = item["output"]
                # Add multiple variations of this comparison question
                variations.append({"instruction": question, "input": "", "output": comp_output})
                variations.append({"instruction": f"Difference between {sec1} and {sec2}", "input": "", "output": comp_output})
                variations.append({"instruction": f"Compare {sec1} and {sec2}", "input": "", "output": comp_output})
                variations.append({"instruction": f"How are {sec1} and {sec2} different?", "input": "", "output": comp_output})
                variations.append({"instruction": f"{sec1} vs {sec2}", "input": "", "output": comp_output})
                break
    
    dataset.extend(variations)
    
    return dataset


def split_dataset(dataset: List[Dict], train_ratio: float = 0.8):
    """Split dataset into train and validation sets"""
    random.shuffle(dataset)
    split_idx = int(len(dataset) * train_ratio)
    return dataset[:split_idx], dataset[split_idx:]


def save_dataset(dataset: List[Dict], output_dir: str = "./data"):
    """Save dataset to files"""
    os.makedirs(output_dir, exist_ok=True)
    
    complete_path = os.path.join(output_dir, "cyber_laws_qa.jsonl")
    with open(complete_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    train_data, val_data = split_dataset(dataset)
    
    train_path = os.path.join(output_dir, "train.jsonl")
    with open(train_path, 'w', encoding='utf-8') as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    val_path = os.path.join(output_dir, "validation.jsonl")
    with open(val_path, 'w', encoding='utf-8') as f:
        for item in val_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    stats = {
        "total_examples": len(dataset),
        "train_examples": len(train_data),
        "validation_examples": len(val_data),
        "avg_instruction_length": sum(len(item["instruction"]) for item in dataset) / len(dataset),
        "avg_output_length": sum(len(item["output"]) for item in dataset) / len(dataset),
        "topics_covered": [
            "Section 43 - Unauthorized Access",
            "Section 43A - Data Protection",
            "Section 66 - Computer Offenses",
            "Section 66B - Receiving Stolen Resources",
            "Section 66C - Identity Theft",
            "Section 66D - Cheating by Personation",
            "Section 66E - Privacy Violation",
            "Section 66F - Cyber Terrorism",
            "Section 67/67A/67B - Obscene Content",
            "Section 69 - Government Powers",
            "Section 70 - Protected Systems",
            "Section 72/72A - Privacy and Confidentiality",
            "Section 75 - Extra-territorial Jurisdiction",
            "Section 79 - Intermediary Liability",
            "General Cybersecurity Topics",
            "CERT-In",
            "Reporting Crimes",
            "Best Practices"
        ]
    }
    
    stats_path = os.path.join(output_dir, "dataset_stats.json")
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Dataset created successfully!")
    print(f"  Complete dataset: {complete_path} ({len(dataset)} examples)")
    print(f"  Training set: {train_path} ({len(train_data)} examples)")
    print(f"  Validation set: {val_path} ({len(val_data)} examples)")
    print(f"  Statistics: {stats_path}")
    
    return stats


def validate_dataset(dataset_path: str):
    """Validate dataset format"""
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                item = json.loads(line)
                assert "instruction" in item, f"Line {i}: Missing 'instruction' field"
                assert "input" in item, f"Line {i}: Missing 'input' field"
                assert "output" in item, f"Line {i}: Missing 'output' field"
        print(f"✓ Dataset validation passed: {dataset_path}")
        return True
    except Exception as e:
        print(f"✗ Dataset validation failed: {e}")
        return False


def main():
    """Main function to generate dataset"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Cyber Saarthi dataset")
    parser.add_argument("--output-dir", default="./data", help="Output directory for dataset")
    parser.add_argument("--validate", action="store_true", help="Validate existing dataset")
    args = parser.parse_args()
    
    if args.validate:
        print("Validating dataset...")
        validate_dataset(os.path.join(args.output_dir, "cyber_laws_qa.jsonl"))
        validate_dataset(os.path.join(args.output_dir, "train.jsonl"))
        validate_dataset(os.path.join(args.output_dir, "validation.jsonl"))
    else:
        print("Generating Cyber Saarthi dataset...")
        dataset = create_dataset()
        stats = save_dataset(dataset, args.output_dir)
        print(f"\nDataset Statistics:")
        print(f"  Total examples: {stats['total_examples']}")
        print(f"  Training examples: {stats['train_examples']}")
        print(f"  Validation examples: {stats['validation_examples']}")
        print(f"  Average instruction length: {stats['avg_instruction_length']:.1f} characters")
        print(f"  Average output length: {stats['avg_output_length']:.1f} characters")


if __name__ == "__main__":
    main()
