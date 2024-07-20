import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import MenuIcon from '@mui/icons-material/Menu';
import PendingTab from '../tab/PendingTab';
import HistoryTab from '../tab/HistoryTab';
import { Box, CssBaseline, Divider, Drawer, FormControlLabel, IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemText, styled, Switch, Toolbar, useTheme } from '@mui/material';
import { ChevronLeftRounded, ChevronRightRounded, PendingActionsRounded, ScheduleRounded } from '@mui/icons-material';
import { ColorModeContext } from '../../App';
import { AppBar } from '../others/AppBar';
import { DrawerHeader } from '../others/DrawerHeader';
import { Main } from '../others/Main';

export const drawerWidth = 240;

const AdminApp: React.FC = () => {
  const [open, setOpen] = useState(false);
  const theme = useTheme();

  const toggleDrawer = () => {
    setOpen(!open);
  };

  const { toggleColorMode } = React.useContext(ColorModeContext);

  const handleChangeLightMode = () => {
    toggleColorMode();
  }

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <AppBar position="fixed" open={open}>
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={toggleDrawer}
              edge="start"
              sx={{ mr: 2, ...(open && { display: 'none' }) }}
            >
              <MenuIcon />
            </IconButton>
            <FormControlLabel control={<Switch onChange={handleChangeLightMode} />} label="Dark mode" />
          </Toolbar>
        </AppBar>
        <Drawer
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
            },
          }}
          variant="persistent"
          anchor="left"
          open={open}
        >
          <DrawerHeader>
            <IconButton onClick={toggleDrawer}>
              {theme.direction === 'ltr' ? <ChevronLeftRounded /> : <ChevronRightRounded />}
            </IconButton>
          </DrawerHeader>
          <Divider />
          <List>
            <ListItem disablePadding>
              <ListItemButton component={Link} to="/pending">
                <ListItemIcon>
                  <PendingActionsRounded />
                </ListItemIcon>
                <ListItemText primary="PENDING" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton component={Link} to="/history">
                <ListItemIcon>
                  <ScheduleRounded />
                </ListItemIcon>
                <ListItemText primary="HISTORY" />
              </ListItemButton>
            </ListItem>
          </List>
        </Drawer>
        <Main open={open}>
          <DrawerHeader />
          <Routes>
            <Route path="/pending" element={<PendingTab />} />
            <Route path="/history" element={<HistoryTab />} />
            <Route path="/" element={<HistoryTab />} /> {/* Default route */}
          </Routes>
        </Main>
      </Box>
    </Router>
  );
};

export default AdminApp;
