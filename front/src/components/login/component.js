import React from 'react'
import { Redirect } from 'react-router-dom'
import { Formik, Field, Form } from 'formik'
import { object, string } from 'yup'

import * as defs from '../../defs'
import { FieldStrap } from '../../utils'

import './style.css'


const LoginSchema = object().shape({
    email: string().email("Please provide a valid email").required("This field is required"),
    password: string().required("This fields is required")
})


class LoginForm extends React.Component {
    render () {
        const loginStatus = this.props.loginStatus
        const logUser = this.props.logUser
        return (
            <Formik
                initialValues={{
                    email: "",
                    password: "",
                }}
                validateOnBlur={false}
                validationSchema={LoginSchema}
                onSubmit={(values) => logUser(values.email, values.password)}
            >
                {() => (
                    <div className="login-wrapper m-auto container">
                        <div className="row">
                            <div className="col text-center">
                                <h4>Welcome back !</h4>
                                <h5 className="text-muted">Sign in to your account to continue</h5>
                            </div>
                        </div>
                        <Form noValidate className="p-4">
                                <div className="form-group">
                                    <label htmlFor="email" className="sr-only">Enter your email</label>
                                    <Field component={FieldStrap} name="email" type="email" id="email" className={`form-control ${loginStatus === defs.STATUS.FAILED ? "is-invalid" : ""}`} placeholder="Email" />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="password" className="sr-only">Enter your password</label>
                                    <Field component={FieldStrap} type="password" name="password" id="password" className={`form-control ${loginStatus === defs.STATUS.FAILED ? "is-invalid" : ""}`} placeholder="Password" />
                                </div>
                                <button type="submit" className="btn btn-primary col">Sign in</button>
                                {loginStatus === defs.STATUS.FAILED &&
                                    <div className="row pt-3">
                                        <div className="col text-danger text-center">Bad credentials</div>
                                    </div>
                                }
                        </Form>
                    </div>
                    )
                }
            </Formik>
        )
    }
}

export const Login = ({isLogged, logUser, loginStatus, from}) => {
    if (isLogged === true) return <Redirect to={from || "/nearby"} />
    return (
        <div className="login-body mt-5 h-100 w-100 align-items-center">
            <LoginForm logUser={logUser} loginStatus={loginStatus}/>
        </div>
    )
}