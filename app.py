from flask import Flask,render_template,request
import jsonify
import os
import requests
import pickle
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
app= Flask(__name__,template_folder='Template')
filename="model.pkl"
fileobj=open(filename,'rb')
b= pickle.load(fileobj)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':	
        Gender=request.form['Gender']
        Married=request.form['Married']
        Dependents=request.form['Dependents']
        Education=request.form['Education']
        Self_Employed=request.form['Self_Employed']
        ApplicantIncome=float(request.form['ApplicantIncome'])
        CoapplicantIncome=float(request.form['CoapplicantIncome'])
        Total_incomelog=np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmount=float(request.form['LoanAmount'])
        LoanAmountlog=np.log(LoanAmount)
        Credit_History=float(request.form['Credit_History'])
        Property_Area=request.form['Property_Area']

        #Gender
        if(Gender=="Male"):
            Male=1
        else:
            Male=0
        
        #Married
        if(Married=="Married_yes"):
            Married_yes=1
        else:
            Married_yes=0

        #Dependents
        if(Dependents=="dependent_1"):
            dependent_1=1
            dependent_2=0
            dependent_3=0
        elif(Dependents=="dependent_2"):
            dependent_1=0
            dependent_2=1
            dependent_3=0
        elif(Dependents=="dependent_3+"):
            dependent_1=0
            dependent_2=0
            dependent_3=1
        else:
            dependent_1=0
            dependent_2=0
            dependent_3=0

        #Education
        if(Education=="Not_Graduate"):
            Not_Graduate=1
        else:
            Not_Graduate=0
        
        #Self_Employed
        if(Self_Employed=="Self_Employed_yes"):
            Self_Employed_yes=1
        else:
            Self_Employed_yes=0

        #Property_Area
        if(Property_Area=="Urban"):
            Urban=1
            Semiurban=0
        elif(Property_Area=="SemiUrban"):
            Urban=0
            Semiurban=1
        else:
            Urban=0
            Semiurban=0

        prediction=b.predict([[Credit_History,Male,Semiurban,Urban,Married_yes,Not_Graduate,Self_Employed_yes,dependent_1,dependent_2,dependent_3,LoanAmountlog,Total_incomelog]])
        
        #Print(prediction)
        if(prediction=="N"):
            prediction="You are not Eligible for Getting Loan"
        else:
            prediction="You are Eligible for Getting Loan"

        return render_template("index.html",prediction_text="loan status is {} loan amount in Rs {}".format(prediction,LoanAmount))

           
        

if __name__=='__main__':
    app.run(debug=True)
            