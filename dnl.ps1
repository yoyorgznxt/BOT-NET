# 定义下载函数
function Download-FileInBackground {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Url,
        
        [Parameter(Mandatory=$true)]
        [string]$OutputPath
    )

    Start-Job -ScriptBlock {
        param($Url, $OutputPath)
        
        try {
            Invoke-WebRequest -Uri $Url -OutFile $OutputPath
            Write-Output "文件下载完成: $OutputPath"
        }
        catch {
            Write-Error "下载失败: $_"
        }
    } -ArgumentList $Url, $OutputPath
}

# 使用示例
$url = "https://example.com/file.zip"
$outputPath = ".\file.zip"

Download-FileInBackground -Url $url -OutputPath $outputPath
