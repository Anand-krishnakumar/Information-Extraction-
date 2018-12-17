import spacy
import nltk, re, pprint
from nltk.corpus import wordnet 
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

class EntityMatcher(object):
	name = 'entity_matcher'

	def __init__(self, nlp, terms, label):
		patterns = [nlp.make_doc(text) for text in terms]
		self.matcher = PhraseMatcher(nlp.vocab)
		self.matcher.add(label, None, *patterns)

	def __call__(self, doc):
		matches = self.matcher(doc)
		for match_id, start, end in matches:
			span = Span(doc, start, end, label=match_id)
			doc.ents = list(doc.ents) + [span]
		return doc
def getHypernyms(token):
	hypernyms = []
	synsets = wordnet.synsets(token)
	for synset in synsets:
		for h in synset.hypernyms():
			for l in h.lemmas():
				hypernyms.append(l.name())
	return list(set(hypernyms))
def getHyponyms(token):
	hyponyms = []
	synsets = wordnet.synsets(token)
	for synset in synsets:
		for h in synset.hyponyms():
			for l in h.lemmas():
				hyponyms.append(l.name())
	return list(set(hyponyms))
def getMeronyms(token):
	meronyms = []
	synsets = wordnet.synsets(token)
	for synset in synsets:
		for h in synset.part_meronyms():
			for l in h.lemmas():
				meronyms.append(l.name())
	return list(set(meronyms))
def getHolonyms(token):
	holonyms = []
	synsets = wordnet.synsets(token)
	for synset in synsets:
		for h in synset.member_holonyms():
			for l in h.lemmas():
				holonyms.append(l.name())
	return list(set(holonyms))
if __name__ == '__main__':
	synonyms = {
	'killing' : {'shot','fired','killed','murdered', 'murder', 'killing', 'vote_out', 'cleanup', 'defeat', 'vote_down', 'pour_down', 'drink_down', 'kill', 'obliterate', 'wipe_out', 'sidesplitting', 'pop', 'down', 'toss_off', 'belt_down', 'shoot_down', 'bolt_down', 'violent_death', 'stamp_out', 'putting_to_death'},
	'kidnap' : {'kidnappers', 'kidnapping', 'forcefully','kidnap', 'abduct', 'capture','seize', 'snatch', 'kidnapped', 'abducted', 'captured', 'snatched','hostage', 'ransom', 'taken', 'missing', 'disappearance', 'vanished', 'disappeared'},
	'acquisition' : {'bought','buy','purchased','acquired','acquire','purchase','takeover','merger','selling', 'sold', 'sell'},
	'award' : {"award", "awarded", "Award", "Awarded", "wins", "honored"},
	'scandals' :{"harassment", "affair", "sexual", "rumour", "rumoured", "accused", "accuse", "accuses"},
	'disaster' : {'flood','floods','earthquake','earthquakes','hurricane','hurricanes','storms','storm','landslide','landslides','avalanche','avalanches','tsunami','blizzard','tornado','tornadoes','drought','droughts','thunderstorm','thunderstorms'},
	'injury' : {'injury','injured','injuries', 'ruled', 'out'},
	'diseases':{'outbreak','disease','widespread', 'epidemic', 'pandemic', 'spread', 'deaths'}
	}
	nlp = spacy.load('en_core_web_sm')


	filename = 'corpus.txt'
	#filename = "The bullet responsible for killing Ron Helus from Ventura County during November's mass shooting at the Borderline Bar & Grill was fired by Ian David Long, authorities said Friday."
	file = open(filename, 'r', encoding="utf-8")
	document = file.read()
	articles = document.split('##')
	data = []
	dependency = []
	#Templates 
	template_killing  = dict()
	template_kidnap = dict()
	template_acquisition = dict()
	template_award = dict()
	template_scandal = dict()
	template_diseases = dict()
	template_disaster = dict()
	template_injury = dict()
	template_transfer = dict()
	template_phone = dict()
	instruments = ['.45-caliber semi-automatic pistol','fire_ship', 'brass_knuckles', 'four-pounder', 'Greek_fire', 'battery', 'projectile', 'stun_gun', 'sword', 'slasher', 'blade', 'steel', 'knuckles', 'W.M.D.', 'knuckle_duster', 'gun', 'field_gun', 'hatchet', 'sling', 'light_arm', 'bow', 'knife', 'brass_knucks', 'knucks', 'WMD', 'bow_and_arrow', 'stun_baton', 'flamethrower', 'shaft', 'weapon_of_mass_destruction', 'pike', 'brand', 'field_artillery', 'tomahawk', 'lance', 'cannon', 'spear', 'missile']
	product = ['market-analytics', 'software', 'restaurant', 'operating system Linux', 'music', 'cloud computing']
	fields = ['best', 'innovation', 'computer science', 'football', 'actor', 'acting']
	accusation = ['sexual','harassment', 'affair']
	injury = ['ruptured', 'knee', 'calf', 'injury', 'hamstring','cruciate', 'ligament','anterior ']
	disaster = ['flood','floods','earthquake','earthquakes','hurricane','hurricanes','storms','storm','landslide','landslides','avalanche','avalanches','tsunami','blizzard','tornado','tornadoes','drought','droughts','thunderstorm','thunderstorms']
	disease = ['cholera', 'Flu','infectious', 'diarrheal' ,'illness']
	entity_instruments = EntityMatcher(nlp, instruments, 'INSTRUMENT')
	entity_product = EntityMatcher(nlp, product, 'PRODUCT')
	entity_field = EntityMatcher(nlp, fields, 'FIELD')
	entity_accuse = EntityMatcher(nlp, accusation, 'ACCUSE')
	entity_disaster = EntityMatcher(nlp, disaster, 'DISASTER')
	entity_injury = EntityMatcher(nlp, injury, 'INJURY')
	entity_disease = EntityMatcher(nlp, disease, 'DISEASE')
	nlp.add_pipe(entity_instruments)
	#nlp.add_pipe(entity_product)
	#nlp.add_pipe(entity_field)
	#nlp.add_pipe(entity_accuse)
	#nlp.add_pipe(entity_disaster)
	#nlp.add_pipe(entity_injury)
	#nlp.add_pipe(entity_disease) 
	id = 0
	for article in articles:
		#killing-template
		killing_victim = set()
		killing_perpetrator = set()
		killing_location = set()
		killing_instrument = set()
		killing_date = set()
		#kidnap-template
		kidnap_victim = set()
		kidnap_perpetrator = set()
		kidnap_location = set()
		kidnap_date = set()
		kidnap_ransom = set()
		#acquisition-template
		acq_buyer = set()
		acq_seller = set()
		acq_product = set()
		acq_price = set()
		#award-template
		award_name = set()
		receipient = set()
		field = set()
		award_date = set()
		#scandal-template
		scandal_accused = set()
		scandal_victim = set()
		scandal_accusation = set()
		scandal_date = set()
		#diseases-template
		disease_name = set()
		disease_location = set()
		disease_casuality = set()
		disease_cause = set()
		disease_date = set()
		#disaster-template
		disaster_type = set()
		disaster_location = set()
		disaster_country = set()
		disaster_date = set()
		#injury-template
		player_name = set()
		team = set()
		injury_type = set()
		injury_time = set()
		#transfer-template
		transfer_player = set()
		transfer_team = set()
		transfer_price = set()
		transfer_time = set()
		#phone-template
		phone_company = set()
		phone_model = set()
		phone_date = set()
		phone_location = set()
		id += 1
		sentences = nltk.sent_tokenize(article)
		for sentence in sentences:
			doc = nlp(sentence)
			tokenList = nltk.word_tokenize(sentence)
			killing_person = set()
			kidnap_person = set()
			scandal_person = set()
			acq_org = set()
			date = set()
			location = set()
			ransom = set()
			for word in tokenList:

				#killing template
				if word in synonyms['killing']:
					#print(sentence)
					for ent in doc.ents:
						if ent.label_ == "PERSON":
							killing_person.add(ent.text)
						if ent.label_ == "DATE":
							killing_date.add(ent.text)
						if ent.label_ == "ORG" or ent.label_ == "GPE":
							killing_location.add(ent.text)
						if ent.label_ == "INSTRUMENT":
							killing_instrument.add(ent.text)
						print(ent.text, ent.label_)
					
					if(re.search('(\S+\s+|^)(\S+\s+|)(kills|for killing|was killed|killing|killing of)(\s+\S+|)(\s+\S+|$)', sentence)):
						s = re.search('(\S+\s+|^)(\S+\s+|)(kills|for killing|was killed|killing|killing of)(\s+\S+|)(\s+\S+|$)', sentence).group(0)
						k = nlp(s)

						for seq in k.ents:
							if seq.label_ == 'PERSON':
								for p in killing_person:
									if seq.text in p:
										killing_victim.add(p)
					if(re.search('(\S+\s+|^)(\S+\s+|)(shot|by|fired by|killed himself|killing by|killed by| was killed by)(\s+\S+|)(\s+\S+|$)', sentence)):
						s = re.search('(\S+\s+|^)(\S+\s+|)(shot|by|fired by|killed himself|killing by|killed by| was killed by)(\s+\S+|)(\s+\S+|$)', sentence).group(0)
						k = nlp(s)
						for seq in k.ents:
							if seq.label_ == 'PERSON':
								for p in killing_person:
									if seq.text in p:
										killing_perpetrator.add(p)
				# kidnap template
				if word in synonyms['kidnap']:
					for ent in doc.ents:	
						if ent.label_ == "MONEY":
							s = re.search('[$]'+ ent.text, sentence).group(0)
							kidnap_ransom.add(s)
						if ent.label_ == "PERSON":
							kidnap_person.add(ent.text)
						if ent.label_ == "GPE" or ent.label_ == "NORP":
							kidnap_location.add(ent.text)
						if ent.label_ == "DATE":
							kidnap_date.add(ent.text)
					if(re.search('(\S+\s+|^)(\S+\s+|)(was held hostage|was kidnapped|was taken|kidnapping| kidnapping a)(\S+\s+|)', sentence)):
						s = re.search('(\S+\s+|^)(\S+\s+|)(was kidnapped|was taken|kidnapping| kidnapping a)(\S+\s+|)', sentence).group(0)
						k = nlp(s)
						for seq in k.ents:
							if seq.label_ == 'PERSON':
								for p in kidnap_person:
									if seq.text in p:
										kidnap_victim.add(p)
						for p in kidnap_person:
							if p not in kidnap_victim:
								kidnap_perpetrator.add(p)
					

				# Acquisition Template
				if word in synonyms['acquisition']:
					for ent in doc.ents:	
						if ent.label_ == "MONEY":
							acq_price.add(ent.text)
						if ent.label_ == "ORG":
							acq_org.add(ent.text)
						if ent.label_ =="PRODUCT":
							acq_product.add(ent.text)
						if(re.search('\w*\s(is selling|is acquired|is bought)\s\w*',sentence)):
							s = re.search('\w*\s(is selling|is acquired|is bought)',sentence).group(0)
							k = nlp(s)
							for seq in k.ents:
								if seq.label_ == 'ORG':
									for p in acq_org:
										if seq.text in p:
											acq_seller.add(p)
							for p in acq_org:
								if p not in acq_seller:
									acq_buyer.add(p)
						
						
				#Award Template
				if word in synonyms['award']:
					for ent in doc.ents:
						if ent.label_ == "DATE":
							award_date.add(ent.text)
						if ent.label_ == "EVENT":
							award_name.add(ent.text)
						if ent.label_ == "FIELD":
							field.add(ent.text)
						if ent.label_ == "PERSON":
							receipient.add(ent.text)
						
				#scandal template
				if word in synonyms['scandals']:
					for ent in doc.ents:
						if ent.label_ == 'DATE':
							scandal_date.add(ent.text)
						if ent.label_ == "PERSON":
							scandal_person.add(ent.text)
						if ent.label_ == "ACCUSE":
							scandal_accusation.add(ent.text)
						
						if(re.search('(\S+\s+|^)(\S+\s+|)(is accused|was accused)(\s+\S+|)(\s+\S+|$)', sentence)):
							s = re.search('(\S+\s+|^)(\S+\s+|)(is accused|was accused)(\s+\S+|)(\s+\S+|$)', sentence).group(0)
							k = nlp(s)

							for seq in k.ents:
								if seq.label_ == 'PERSON':
									for p in scandal_person:
										if seq.text in p:
											scandal_accused.add(p)
									for p in scandal_person:
										if p not in scandal_accused:
											scandal_victim.add(p)
				if word in synonyms['disaster']:
					for ent in doc.ents:
						if ent.label_ == 'DATE':
							disaster_date.add(ent.text)
						if ent.label_ == "LOC":
							disaster_location.add(ent.text)
						if ent.label_ == "GPE":
							disaster_country.add(ent.text)
						if ent.label_ == "DISASTER":
							disaster_type.add(ent.text)

						
				if word in synonyms['injury']:
					for ent in doc.ents:
						if ent.label_ == "PERSON":
							player_name.add(ent.text)
						if ent.label_ == "INJURY":
							injury_type.add(ent.text)
						if ent.label_ == "ORG":
							team.add(ent.text)
						if ent.label_ == "DATE":
							injury_time.add(ent.text)
						
				if word in synonyms['diseases']:
					for ent in doc.ents:
						if ent.label_ == "DISEASE":
							disease_name.add(ent.text)
							disease_cause.add(ent.text)
						if ent.label_ == "GPE":
							disease_location.add(ent.text)
						if ent.label_ == "CARDINAL":
							disease_casuality.add(ent.text) 
						if ent.label == "DATE":
							disease_date.add(ent.text)

			template_killing[id] = ({
				'Victim' : ' '.join(killing_victim),
				'perpetrator': ' '.join(killing_perpetrator),
				'Location' : ' '.join(killing_location),
				'Instrument': ' '.join(killing_instrument),
				'Date' : ' '.join(killing_date)
				})			
			template_kidnap[id] = ({
				'Victim' : ' '.join(kidnap_victim),
				'perpetrator': ' '.join(kidnap_perpetrator),
				'Location' : ' '.join(kidnap_location),
				'Date' : ' '.join(kidnap_date),
				'Ransom':' '.join(kidnap_ransom)
				})	
			template_acquisition[id] = ({
				'Buyer' : ' '.join(acq_buyer),
				'Seller': ' '.join(acq_seller),
				'Product' : ' '.join(acq_product),
				'Price' : ' '.join(acq_price)
				})
			template_award[id] = ({
				'Award_Name' : ' '.join(award_name),
				'Receipient': ' '.join(receipient),
				'Field' : ' '.join(field),
				'Date' : ' '.join(award_date)
				})	
			template_scandal[id] = ({
				'Accused' : ' '.join(scandal_accused),
				'Victim': ' '.join(scandal_victim),
				'Accusation' : ' '.join(scandal_accusation),
				'Date' : ' '.join(scandal_date)
				})
			template_transfer[id] = ({
				'Victim' : ' '.join(kidnap_victim),
				'perpetrator': ' '.join(kidnap_perpetrator),
				'Location' : ' '.join(kidnap_location),
				'Date' : ' '.join(kidnap_date),
				'Ransom':' '.join(kidnap_ransom)
				})	
			template_injury[id] = ({
				'Player_name' : ' '.join(player_name),
				'Team': ' '.join(team),
				'Injury_type' : ' '.join(injury_type),
				'Time_to_recover' : ' '.join(injury_time)
				})
			template_phone[id] = ({
				'Victim' : ' '.join(kidnap_victim),
				'perpetrator': ' '.join(kidnap_perpetrator),
				'Location' : ' '.join(kidnap_location),
				'Date' : ' '.join(kidnap_date),
				'Ransom':' '.join(kidnap_ransom)
				})	
			template_disaster[id] = ({
				'Type' : ' '.join(disaster_type),
				'Location' : ' '.join(disaster_location),
				'Country' : ' '.join(disaster_country),
				'Date': ' '.join(disaster_date)
				})
			template_diseases[id] = ({
				'Name' : ' '.join(disease_name),
				'Location': ' '.join(disease_location),
				'Casualities' : ' '.join(disease_casuality),
				'Causes' : ' '.join(disease_cause),
				'Date':' '.join(disease_date)
				})							
			for token in doc:
				#print(token)
				data.append({
					"token": token.text,
					"lemma": token.lemma_,
					"pos": token.pos_ ,
					"tag": token.tag_ ,
					"dependency": token.dep_ ,
					"hypernyms":getHypernyms(str(token)), 
					"holonyms" :getHolonyms(str(token)) ,
					"meronyms" :getMeronyms(str(token)) ,
					"hyponyms" : getHyponyms(str(token))
					})
				dependency.append({
					"Text" :token.text,
					"dependency": token.dep_,
					"Head Text" : token.head.text,
					"Head Pos" : token.head.pos_ ,
					"children" : [child for child in token.children]
					})
				#print(dependency)
				#print(data)
	print(template_killing)
	#print(template_kidnap)
	#print(template_acquisition)
	#print(template_award)
	#print(template_scandal)
	#print(template_disaster)
	#print(template_injury)
	#print(template_diseases)
	#print(template_transfer)
	#print(template_phone)




