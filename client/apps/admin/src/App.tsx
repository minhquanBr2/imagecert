import { createTheme, ThemeProvider } from "@mui/material";
import AdminApp from "./components/pages/Admin";
import React, { useContext } from "react";
import AuthContext, { AuthProvider } from "./context/AuthContext";
import LoginScreen from "./components/pages/Login";

export const ColorModeContext = React.createContext({ toggleColorMode: () => {} });
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
    const [mode, setMode] = React.useState<'light' | 'dark'>('light');
    const colorMode = React.useMemo(
      () => ({
        toggleColorMode: () => {
          setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
        },
      }),
      [],
    );
  
    const theme = React.useMemo(
      () =>
        createTheme({
          palette: {
            mode,
          },
        }),
      [mode],
    );
  
  const { user } = useContext(AuthContext);
  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
          {user ? <AdminApp /> : <LoginScreen />}
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};

export default App;
