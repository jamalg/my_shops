import React from 'react'
import { Redirect } from 'react-router-dom'
import { Formik, Field, Form } from 'formik'
import { object, string } from 'yup'

import * as api from '../../api'
import { FieldStrap, validate } from '../../utils'

import './style.css'

const getRegisterSchema = (values) => {
    return object().shape({
        firstName: string().required("This field is required"),
        lastName: string().required("This field is required"),
        email: string().email("Please provide a valid email").required("This field is required"),
        password: string()
            .required("This field is required")
            .min(8, "Too short. Password should be between 8 to 20 characters.")
            .max(20, "Too long. Password should be between 8 to 20 characters.")
            .matches(/\d/, "At least a digit")
            .matches(/\W/, "At least a special character")
            .matches(/[a-z]/, "At least one lowercase character")
            .matches(/[A-Z]/, "At least one uppercase character"),
        passwordConfirm: string()
            .required("This field is required")
            .oneOf([values.password], "Passwords do not match"),
    })
}


class RegisterForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            redirectToLogin: false,
            willBeRedirected: false,
        }
    }
    render () {
        const redirectToLogin = this.state.redirectToLogin
        if (redirectToLogin === true) return <Redirect to="/login"/>

        const willBeRedirected = this.state.willBeRedirected
        if (willBeRedirected === true) return (
            <div className="text-center">
                <h2 className="text-success">Congratulations !</h2>
                <p className="lead">
                    You will be redirected to login !
                </p>
            </div>
        )

        return (
            <Formik
                initialValues={{
                    firstName: "",
                    lastName: "",
                    email: "",
                    password: "",
                    passwordConfirm: "",
                }}
                validateOnBlur={true}
                validate={validate(getRegisterSchema)}
                onSubmit={(values, { setSubmitting, setErrors}) => {
                    return api.registerUser(values)
                        .then(() => {
                            setTimeout(() => this.setState({redirectToLogin: true}), 1500)
                            this.setState({willBeRedirected: true})
                        }, (errors) => {
                            setSubmitting(false)
                            setErrors(errors)
                        })
                }}
            >
                {({isSubmitting}) => (
                    <div className="register-wrapper m-auto container">
                        <div className="row text-center">
                            <div className="col">
                                <h4>Get started</h4>
                                <h5 className="text-muted">Fill this form to start using <span style={{fontWeight: "italic"}}>Shops</span></h5>
                            </div>
                        </div>
                        <Form noValidate className="p-2">
                            <fieldset>
                                <legend>About you</legend>
                                <div className="form-row">
                                    <div className="form-group col-sm">
                                        <label htmlFor="firstName" className="sr-only">First name</label>
                                        <Field component={FieldStrap} id="firstName" type="text" className="form-control" name="firstName" placeholder="First name" />
                                    </div>
                                    <div className="form-group col-sm">
                                        <label htmlFor="lastName" className="sr-only">Last name</label>
                                        <Field component={FieldStrap} id="lastName" type="text" className="form-control" name="lastName" placeholder="Last name" />
                                    </div>
                                </div>
                                <div className="form-group">
                                        <label htmlFor="email" className="sr-only">Email</label>
                                        <Field component={FieldStrap} id="email" type="email" className="form-control" name="email" aria-describedby="emailText" placeholder="Email" />
                                        <small id="emailText" className="text-from text-muted">This email will serve as you identifier</small>
                                </div>
                            </fieldset>
                            <fieldset required>
                                <legend>Security</legend>
                                <div className="form-row">
                                    <div className="from-group col-sm">
                                        <label htmlFor="password" className="sr-only">Password</label>
                                        <Field component={FieldStrap} id="password" type="password" className="form-control" name="password" aria-describedby="passwordText" required/>
                                        <small id="passwordText" className="text-from text-muted">Choose a strong password !</small>
                                    </div>
                                    <div className="from-group col-sm">
                                        <label htmlFor="passwordConfirm" className="sr-only">Confirm Password</label>
                                        <Field component={FieldStrap} id="passwordConfirm" type="password" className="form-control" name="passwordConfirm" aria-describedby="passwordConfirmText" required/>
                                        <small id="passwordConfirmText" className="text-from text-muted">Confirm your password</small>
                                    </div>
                                </div>
                            </fieldset>
                            <button type="submit" className="btn btn-primary w-100 mt-3" disable={isSubmitting.toString()}>Sign Up !</button>
                        </Form>
                    </div>
                    )
                }
            </Formik>
        )
    }
}

export const Register = () => {
    return (
        <div className="register-body mt-5 h-100 w-100 align-items-center">
            <RegisterForm />
        </div>
    )
}