import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FooterComponent } from './layout/footer.component';
import { HeaderComponent } from './layout/header.component';
import { AboutComponent } from './pages/about.component';
import { CateringComponent } from './pages/catering.component';
import { ContactComponent } from './pages/contact.component';
import { GalleryComponent } from './pages/gallery.component';
import { HomeComponent } from './pages/home.component';
import { MenuComponent } from './pages/menu.component';
import { OrderOnlineComponent } from './pages/order-online.component';
import { PrivateEventsComponent } from './pages/private-events.component';
import { IconComponent } from './shared/icon.component';
import { InquiryFormComponent } from './shared/inquiry-form.component';
import { LogoComponent } from './shared/logo.component';
import { PageHeroComponent } from './shared/page-hero.component';
import { WaveComponent } from './shared/wave.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    IconComponent,
    WaveComponent,
    LogoComponent,
    PageHeroComponent,
    InquiryFormComponent,
    HomeComponent,
    MenuComponent,
    AboutComponent,
    PrivateEventsComponent,
    OrderOnlineComponent,
    CateringComponent,
    GalleryComponent,
    ContactComponent,
  ],
  imports: [BrowserModule, FormsModule, AppRoutingModule],
  bootstrap: [AppComponent],
})
export class AppModule {}
