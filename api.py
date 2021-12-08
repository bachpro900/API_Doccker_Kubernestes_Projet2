from fastapi import FastAPI
import uvicorn
from input_data_model import Nouvelle_transaction
import pickle
from catboost import CatBoostClassifier
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import base64


# ####### importer le modèle ML ########## #
##########################################
model = pickle.load(open("fraud_model.pkl", 'rb'))
catboostclassifier_model = pickle.load(open("fraud_CatBoostClassifier_model.pkl", "rb"))

#définir l'API
api = FastAPI(
            title='API fraud',
            description="API sur la detection des transacations bancaires fraduleuses",
            version="1.0.1")

#définir l'authentification
security = HTTPBasic()
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):

    #fonction pour encoder les mots de passe
    
    def encoder(mdp):
        b = mdp.encode("UTF-8")
        e = base64.b64encode(b)
        s = e.decode("UTF-8")        
        return s


    bdd_utilisateur = {"Bachir": "YmFjaGlyMTIz", "Ali": "YXRtYW5pMTIz" , "API_Fraud": "YXBpZnJhdWQxMjM="}

    correct_username = False
    correct_password = False
    if ((secrets.compare_digest(credentials.username, list(bdd_utilisateur.keys())[0] ) and 
    secrets.compare_digest(encoder(credentials.password), list(bdd_utilisateur.values())[0])) or
    (secrets.compare_digest(credentials.username, list(bdd_utilisateur.keys())[1] ) and 
    secrets.compare_digest(encoder(credentials.password), list(bdd_utilisateur.values())[1])) or
    (secrets.compare_digest(credentials.username, list(bdd_utilisateur.keys())[2] ) and 
    secrets.compare_digest(encoder(credentials.password), list(bdd_utilisateur.values())[2]))    
    ):
        correct_username = True
        correct_password = True
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},)

    return credentials.username

       
@api.get("/user")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}




# premire route
@api.get('/', name= "Vérifier si l'API est fonctionnelle")
def is_functionnal(username: str = Depends(get_current_username)):
    """On vrifie si l'API est fonctionnelle."""
    return "l'API fonctionne correctement :)"


# nouvelle transaction
@api.put('/nouvelle_transaction', name='Vérifier si la nouvelle transaction est frauduleuse')
def get_is_transaction_fraud(transaction: Nouvelle_transaction, username: str = Depends(get_current_username)):
    """On vérifie si une transaction est frauduleuse en remplissant les pramètres ci-dessous. Tout les paramètres, comme purchase_value, sex ...ect. sont à renseigner."""

    trans_input = [t[1] for t in transaction]
    
    
    #prédiction avec le model kmeans
    model_prediction = model.predict([trans_input])
    
    #prediction avec le model de CatBoostClassifier:
    catboostclassifier_prediction = catboostclassifier_model.predict([trans_input])
    
    # affichage des résultats avec les kmeans
    modele_kmeans = '''Resultat de la transaction avec le modèle des Kmeans :'''
    type_kmeans='''- type de la transaction = {transaction_status}'''
    proba_kmeans='''- probalité = {proba}'''
    retour_a_la_ligne1 ="********************************************"
    retour_a_la_ligne2 ="********************************************"

    if model_prediction[0] == 1:
        transaction_status = "Cette transaction est fradauleuse !" 
        proba = model.predict_proba([trans_input])[0][1]
    else:
        transaction_status = "Cette transaction n'est pas frauduleuse :)"
        proba = model.predict_proba([trans_input])[0][0]
    type_k=type_kmeans.format(transaction_status=transaction_status)
    proba_k=proba_kmeans.format(proba=proba)
    
    
    
    # affichage des résultats avec les CatBoost
    modele_catboost = '''Resultat de la transaction avec le modèle du CatBoostClassifier :'''
    type_catboost='''- type de la transaction = {transaction_status}'''
    proba_catboost='''- probalité = {proba}'''


    
    if catboostclassifier_prediction[0] == 1:
        cat_boost_transaction_status = "Cette transaction est fraduleuse !" 
        cat_boost_proba = catboostclassifier_model.predict_proba([trans_input])[0][1]
    else:
        cat_boost_transaction_status = "Cette transaction n'est pas fraduleuse :)"
        cat_boost_proba = catboostclassifier_model.predict_proba([trans_input])[0][0]
    type_cat=type_catboost.format(transaction_status=cat_boost_transaction_status)
    proba_cat=proba_catboost.format(proba=cat_boost_proba)

    
    return modele_kmeans, type_k, proba_k,retour_a_la_ligne1, retour_a_la_ligne2,  modele_catboost, type_cat, proba_cat






# nouvelle transaction
@api.get('/api_test', name="tester l'API ", include_in_schema=False)
def get_is_transaction_fraud(transaction: Nouvelle_transaction):
    trans_input = [t[1] for t in transaction]
    # prédiction avec le model kmeans
    model_prediction = model.predict([trans_input])
    #prediction avec le model de CatBoostClassifier:
    catboostclassifier_prediction = catboostclassifier_model.predict([trans_input])
    # affichage des résultats avec les kmeans
    modele_kmeans = '''
    Resultat de la transaction avec le modèle des Kmeans :'''
    type_kmeans='''
    - type de la transaction = {transaction_status}'''
    proba_kmeans='''
    - probalité = {proba}'''
    retour_a_la_ligne1 ="********************************************"
    retour_a_la_ligne2 ="********************************************"
    if model_prediction[0] == 1:
        transaction_status = "Cette transaction est fraduleuse !" 
        proba = model.predict_proba([trans_input])[0][1]
    else:
        transaction_status = "Cette transaction n'est pas fraduleuse :)"
        proba = model.predict_proba([trans_input])[0][0]
    type_k=type_kmeans.format(transaction_status=transaction_status)
    proba_k=proba_kmeans.format(proba=proba)
    # affichage des résultats avec les CatBoost
    modele_catboost = ''''
    Resultat de la transaction avec le modèle du CatBoostClassifier :'''
    type_catboost='''
    - type de la transaction = {transaction_status}'''
    proba_catboost='''
    - probalité = {proba}'''
    if catboostclassifier_prediction[0] == 1:
        cat_boost_transaction_status = "Cette transaction est fraduleuse !" 
        cat_boost_proba = catboostclassifier_model.predict_proba([trans_input])[0][1]
    else:
        cat_boost_transaction_status = "Cette transaction n'est pas fraduleuse :)"
        cat_boost_proba = catboostclassifier_model.predict_proba([trans_input])[0][0]
    type_cat=type_catboost.format(transaction_status=cat_boost_transaction_status)
    proba_cat=proba_catboost.format(proba=cat_boost_proba)
    return modele_kmeans, type_k, proba_k,retour_a_la_ligne1, retour_a_la_ligne2,  modele_catboost, type_cat, proba_cat



if __name__ == '__main__':
    uvicorn.run(api, host="0.0.0.0", port=8080)

