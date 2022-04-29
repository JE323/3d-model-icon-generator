using System;
using System.Data;

namespace thumbnailService.Models;

public partial class InlineResponse200
{
    public InlineResponse200() => Success = DateTimeOffset.Now;
}