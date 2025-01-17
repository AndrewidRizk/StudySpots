import styles from '../styles/Header.module.css';
import InfoPanel from "./InfoPanel";
import Image from "next/image";

export default function Header() {
    return (
        <header className={styles.header}>
            <h1 className={styles.title}>
            <a href="https://study-spots-3fgv.vercel.app/">
            <Image
                src="/images/logo.png" // Path to your logo in the public folder
                alt="Logo"
                width={60} // Adjust based on font size
                height={60} // Adjust based on font size
                className={styles.logo}
            />
            </a>
            Spots
            <InfoPanel/>
            </h1>
            
            <h2 className={styles.headerSubtitle}>Powered by <a href="https://yorku.dev/" className={styles.link} target="_blank" rel="noopener noreferrer">SSADC</a></h2>
        </header>
    );
}
