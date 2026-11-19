/*
 * Golden Wok site content.
 *
 * NOTE: The business name, address, phone, hours and menu below come from the
 * concept mockups and are FICTIONAL PLACEHOLDERS. Replace them with verified
 * details before going live.
 */

export interface NavLink {
  label: string;
  path: string;
}

export interface HoursRow {
  days: string;
  time: string;
}

export interface MenuItem {
  name: string;
  description: string;
}

export interface MenuSection {
  id: string;
  title: string;
  icon: string;
  image?: string;
  imageAlt?: string;
  items: MenuItem[];
}

export interface Dish {
  name: string;
  image: string;
  description?: string;
}

export interface GalleryImage {
  src: string;
  alt: string;
}

export const SITE = {
  name: 'Golden Wok',
  tagline: 'Chinese Restaurant',
  street: '12345 Forest Hill Blvd',
  cityLine: 'Wellington, FL 33414',
  phone: '(561) 555-6888',
  phoneHref: 'tel:+15615556888',
  email: 'hello@goldenwok.example',
  // Replace with your online-ordering provider link when one exists.
  orderUrl: 'tel:+15615556888',
  mapsUrl: 'https://www.google.com/maps/search/?api=1&query=12345+Forest+Hill+Blvd+Wellington+FL+33414',
  facebookUrl: 'https://www.facebook.com/',
  instagramUrl: 'https://www.instagram.com/',
  hours: [
    { days: 'Mon – Thu', time: '11:00 AM – 9:30 PM' },
    { days: 'Fri – Sat', time: '11:00 AM – 10:00 PM' },
    { days: 'Sun', time: '12:00 PM – 9:00 PM' },
  ] as HoursRow[],
};

export const NAV: NavLink[] = [
  { label: 'Home', path: '/' },
  { label: 'Menu', path: '/menu' },
  { label: 'About', path: '/about' },
  { label: 'Private Events', path: '/private-events' },
  { label: 'Catering', path: '/catering' },
  { label: 'Gallery', path: '/gallery' },
  { label: 'Contact', path: '/contact' },
];

export const POPULAR: Dish[] = [
  { name: 'Orange Chicken', image: 'assets/img/orange-chicken.jpg', description: 'Tender chicken tossed in a zesty orange glaze.' },
  { name: 'Beef with Broccoli', image: 'assets/img/beef-broccoli.jpg', description: 'Sliced beef and fresh broccoli in a savory brown sauce.' },
  { name: 'Kung Pao Shrimp', image: 'assets/img/kung-pao-shrimp.jpg', description: 'Shrimp, peanuts, bell peppers and scallions in a spicy-sweet sauce.' },
];

export const MENU: MenuSection[] = [
  {
    id: 'starters',
    title: 'Starters & Dim Sum',
    icon: 'bowl',
    image: 'assets/img/dumplings.jpg',
    imageAlt: 'Steamed dumplings in a bamboo basket',
    items: [
      { name: 'Pork Dumplings (6)', description: 'Pan-seared or steamed, served with house sauce.' },
      { name: 'Vegetable Spring Rolls (2)', description: 'Crispy rolls filled with fresh vegetables.' },
      { name: 'Crab Rangoon (6)', description: 'Crispy wontons with a creamy crab filling.' },
      { name: 'Edamame', description: 'Steamed soybeans with sea salt.' },
      { name: 'Chicken Lettuce Wraps', description: 'Minced chicken, vegetables and hoisin sauce, served with crisp lettuce.' },
    ],
  },
  {
    id: 'specialties',
    title: 'Chef’s Specialties',
    icon: 'cloche',
    image: 'assets/img/general-tso.jpg',
    imageAlt: 'General Tso’s chicken with broccoli',
    items: [
      { name: 'General Tso’s Chicken', description: 'Crispy chicken in a sweet and savory sauce.' },
      { name: 'Orange Chicken', description: 'Tender chicken tossed in a zesty orange glaze.' },
      { name: 'Mongolian Beef', description: 'Sliced beef with scallions in a rich, savory sauce.' },
      { name: 'Sesame Chicken', description: 'Crispy chicken with a honey sesame glaze.' },
      { name: 'Happy Family', description: 'A delicious combination of chicken, beef, shrimp and fresh vegetables in a classic brown sauce.' },
    ],
  },
  {
    id: 'noodles',
    title: 'Noodles & Rice',
    icon: 'noodles',
    image: 'assets/img/lo-mein.jpg',
    imageAlt: 'Shrimp lo mein in a dark bowl',
    items: [
      { name: 'Lo Mein', description: 'Soft egg noodles with your choice of chicken, beef, shrimp or vegetables.' },
      { name: 'Chow Mein', description: 'Stir-fried vegetables with your choice of chicken, beef, shrimp or pork.' },
      { name: 'Fried Rice', description: 'Classic fried rice with egg, peas, carrots and scallions. Choice of chicken, pork, beef or shrimp.' },
    ],
  },
  {
    id: 'seafood',
    title: 'Seafood & Vegetables',
    icon: 'shrimp',
    image: 'assets/img/shrimp-broccoli.jpg',
    imageAlt: 'Shrimp with broccoli and red peppers',
    items: [
      { name: 'Shrimp with Broccoli', description: 'Jumbo shrimp and fresh broccoli in a savory garlic sauce.' },
      { name: 'Kung Pao Shrimp', description: 'Shrimp, peanuts, bell peppers and scallions in a spicy-sweet sauce.' },
      { name: 'Szechuan Vegetables', description: 'A vibrant mix of fresh vegetables with a classic Szechuan sauce.' },
      { name: 'Buddha’s Delight', description: 'Seasonal vegetables stir-fried in a light, flavorful sauce.' },
    ],
  },
  {
    id: 'lunch',
    title: 'Lunch Specials',
    icon: 'leaf',
    image: 'assets/img/wok-fire.jpg',
    imageAlt: 'Chef tossing vegetables in a flaming wok',
    items: [
      { name: 'Served Mon – Sat, 11:00 AM – 3:00 PM', description: 'Each special comes with fried rice and your choice of soup or an egg roll.' },
      { name: 'Chicken with Broccoli', description: 'Light and savory, a lunchtime favorite.' },
      { name: 'Sweet & Sour Chicken', description: 'Crispy chicken with pineapple and peppers.' },
      { name: 'Pepper Steak', description: 'Sliced beef with onions and green peppers.' },
    ],
  },
];

export const GALLERY: GalleryImage[] = [
  { src: 'assets/img/g1.jpg', alt: 'Orange chicken garnished with orange slices' },
  { src: 'assets/img/g2.jpg', alt: 'Dining room with lanterns and carved wooden screens' },
  { src: 'assets/img/g3.jpg', alt: 'Kung pao shrimp with peppers' },
  { src: 'assets/img/g4.jpg', alt: 'Steamed soup dumplings in a bamboo basket' },
  { src: 'assets/img/g5.jpg', alt: 'Table set beside a carved screen and pink orchids' },
  { src: 'assets/img/g6.jpg', alt: 'Spring rolls with sweet chili sauce' },
  { src: 'assets/img/dining-room.jpg', alt: 'Dining room with orchids and red lanterns' },
  { src: 'assets/img/chef.jpg', alt: 'Chef cooking over a flaming wok' },
  { src: 'assets/img/private-room.jpg', alt: 'Private dining room set for a celebration' },
];
