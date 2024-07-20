import React, { useState } from 'react';
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
  const [open, setOpen] = React.useState(false);
  const [selectedTab, setSelectedTab] = useState<number>(0);
  const theme = useTheme();

  const toggleDrawer = () => {
    setOpen(!open);
  };

  const handleTabChange = (tab: number) => {
    setSelectedTab(tab);
    setOpen(false);
  };

  const { toggleColorMode } = React.useContext(ColorModeContext);

  const handleChangeLightMode = () => {
      toggleColorMode();
  }
    

  return (
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
          <ListItem key="Pending" disablePadding>
            <ListItemButton onClick={() => handleTabChange(0)}>
              <ListItemIcon>
                <PendingActionsRounded />
              </ListItemIcon>
              <ListItemText primary="PENDING" />
            </ListItemButton>
          </ListItem>
          <ListItem key="History" disablePadding>
            <ListItemButton onClick={() => handleTabChange(1)}>
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
        {selectedTab === 0 ? <PendingTab /> : <HistoryTab />}
      </Main>
    </Box>
  );
};

export default AdminApp;
