import System.Environment (getArgs)
import Data.List (intercalate)
import Text.Regex.TDFA

tokenize :: String -> [String]
tokenize content = getAllTextMatches $ content =~ ("\\w+" :: String)


main :: IO ()
main = do
    args <- getArgs
    case args of
        [inputFile, outputFile] -> do
            content <- readFile inputFile
            let wordList = tokenize content
            writeFile outputFile (intercalate "\n" wordList)
            putStrLn $ "Word list written to " ++ outputFile
        _ -> putStrLn "Usage ./program inputFile outputFile"
    

