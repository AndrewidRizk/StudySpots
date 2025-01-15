import styles from '../styles/Header.module.css';
import InfoPanel from "./InfoPanel";

export default function Header() {
    return (
        <header className={styles.header}>
            <h1 className={styles.title}>
            <span className={styles.highlight}>YU</span>Sports
            </h1>
            <InfoPanel info="Bla Bla bla bla bla bla bla bla bla bla bla bla bla bla" />
        </header>
    );
}
