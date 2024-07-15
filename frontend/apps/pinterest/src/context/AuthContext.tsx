import React, { Component } from 'react'
import { AuthContextInterface, AuthT } from '../interface/Auth'
import { AUTH_KEY } from '../type/constant'
import { getAuth, signOut } from 'firebase/auth'

const AuthContext = React.createContext<AuthContextInterface>({
	logIn: () => null,
	logOut: () => null,
	user: null,
})

type Props = {
	children?: JSX.Element | JSX.Element[]
	logIn?: () => null
	logOut?: () => null
}

type State = {
	user: AuthT | null
}

export class AuthProvider extends Component<Props, State> {
	constructor(props: Props) {
		super(props)

		this.state = {
			user: localStorage.getItem(AUTH_KEY) ? JSON.parse(localStorage.getItem(AUTH_KEY) as string) : null,
		}
	}

	logIn = (user: AuthT) => {
		this.setState({
			user: user,
		})
	}

	logOut = () => {
		const auth = getAuth();
		signOut(auth).then(() => {
			this.setState({
				user: null,
			})
		}).catch((error) => {
			console.log('logout error: ', error)
		});
	}

	render() {
		const { user } = this.state
		const { logOut, logIn } = this
		console.log('user: ', user)
		return (
			<AuthContext.Provider
				value={{ user, logIn, logOut }}>
				{this.props.children}
			</AuthContext.Provider>
		)
	}
}

export const AuthConsumer = AuthContext.Consumer
export default AuthContext