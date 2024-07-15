
export interface AuthT {
	email: string
	displayName: string
	uid: string
	photoURL: string
}

export interface AuthContextInterface {
	user: AuthT | null
	logIn: (user: AuthT) => void
	logOut: () => void
}